import bpy, os
from re import (search, IGNORECASE)
from bpy_extras.io_utils import ImportHelper

from bpy.props import (
    EnumProperty,
    FloatProperty,
    BoolProperty,
    StringProperty,
)

bl_info = {
    "name": "Redshift Material Builder",
    "description": "Create quick PBR materials with Redshift",
    "author": "Abrasic",
    "version": (1, 4),
    "blender": (3, 5, 0),
    "location": "Shader Editor > N-Panel > RMB",
    "support": "COMMUNITY",
    "category": "Node",
}

material_group = ["base_color","ao","metallic","specular","gloss","rough","transmission","sss","normal","bump","emission","alpha", "displacement"]
material_dir_group = ["dir_color","dir_ao","dir_metallic","dir_specular","dir_gloss","dir_rough","dir_transmission","dir_sss","dir_normal","dir_bump","dir_emission","dir_alpha", "dir_displacement"]
image_node_matches = []

class RMB_props(bpy.types.PropertyGroup):
    
    ## Create
    
    base_dir: StringProperty (
        update=lambda self, context: updateList(),
        name="Folder",
        description="Folder that contains all your desired texture files",
        default="",
        subtype = "DIR_PATH")
        
    file_filter: StringProperty (
        update=lambda self, context: updateList(),
        name="Filter",
        description="Only search for textures that include AT LEAST ONE of the words entered. Separate words with spaces",
        default="",)  
      
    dir_color: StringProperty (
        name="Base Color",
        description="",
        default="")  
        
    dir_ao: StringProperty (
        name="AO",
        description="",
        default="")  
        
    dir_metallic: StringProperty (
        name="Metallic",
        description="",
        default="")  
        
    dir_specular: StringProperty (
        name="Specular",
        description="",
        default="")  
        
    dir_gloss: StringProperty (
        name="Gloss",
        description="",
        default="")  
        
    dir_rough: StringProperty (
        name="Roughness",
        description="",
        default="")  
        
    dir_transmission: StringProperty (
        name="Transmission",
        description="",
        default="")  
        
    dir_sss: StringProperty (
        name="SSS",
        description="",
        default="")  
        
    dir_normal: StringProperty (
        name="Normal",
        description="",
        default="")  

    dir_bump: StringProperty (
        name="Bump",
        description="",
        default="")  

    dir_emission: StringProperty (
        name="Emission",
        description="",
        default="")  

    dir_alpha: StringProperty (
        name="Alpha",
        description="",
        default="")   
        
    dir_displacement: StringProperty (
        name="Displacement",
        description="",
        default="")   
        
    ## Settings

    scalar_node: BoolProperty(
        name="Add Vector for Texture Scale",
        description="When enabled, a Vector input will be connected to all texture scales. This is useful for scaling all textures at once if your PBR material appears too big or too small",
        default=False
    )
    
    image_node: BoolProperty(
        name="Add Image Texture Node",
        description="When enabled, this will add an Image Texture node to the side of your node tree for your color texture. Without it, your material will appear white in the viewport",
        default=True
    )
    
    correct_node: BoolProperty(
        name="Add rsColorCorrect for Color",
        description="When enabled, this will connect your color texture thru an rsColorCorrect node",
        default=False
    )

    color_is_alpha: BoolProperty(
        name="Diffuse is Alpha",
        description="When enabled, the Alpha of the material will be determined by the alpha channel of the base color texture",
        default=False
    )
    
    color_spaces = bpy.types.Image.bl_rna.properties['colorspace_settings'].fixed_type.properties['name'].enum_items
    color_items = []
    
    for i, space in enumerate(color_spaces):
        color_items.append((space.name, space.name, "", i))
    
    color_space: EnumProperty(
        name="Diffuse",
        description="Sets the color space for your color texture",
        items=color_items,
        default='sRGB'
    )
    
    normal_type: EnumProperty(
        name="Normal Input",
        description="Sets the RS Bump node to this input type for its normal maps. This also affects displacement map type, if used",
        items=[('1', "Tangent-Space", "",),('2', "Object-Space", ""),],
        default=0
    )
    
    alpha_type: EnumProperty(
        name="Alpha Input",
        description="Sets the Sprite node to this input type for its alpha maps",
        items=[('0', "From Color Intensity", "",),('1', "From Alpha", ""),],
        default=1
    )

    sss_map_input: EnumProperty(
        name="SSS Input",
        description="Where your Subsurface map will connect to by default",
        items=[('0', "Weight", "",),('1', "Color", ""),('2', "Weight & Color", ""),],
        default=0
    )
    
    normal_scale: FloatProperty(
        name="Normal Scale",
        description="Sets the value of normal map scale, if used",
        default=1,
        soft_min=-2,
        soft_max=2
    )
    
    bump_scale: FloatProperty(
        name="Bump Scale",
        description="Sets the value of bump map scale, if used",
        default=0.01,
        soft_min=-2,
        soft_max=2
    )
    
    displacement_scale: FloatProperty(
        name="Displacement Scale",
        description="Sets the value of displacement scale, if used",
        default=0.05,
        soft_min=-2,
        soft_max=2
    )
    
    uv_map: StringProperty(
        name="UV Map", 
        default="UVMap", 
        description="The UV Map that will be used on all texture nodes"
    )
    
    use_udim: BoolProperty(
        name="Use UDIM",
        description="When enabled, all texture sources will be set to use UDIM Tiles",
        default=False
    )
        
    base_color: StringProperty(
        name='Base Color',
        default='color col diffuse diff albedo',)
        
    sss: StringProperty(
        name='Subsurface',
        default='sss subsurface',)
        
    metallic: StringProperty(
        name='Metalness',
        default='mtl metal metallic metalness',)
        
    specular: StringProperty(
        name='Specular',
        default='specularity specular spec spc',)
        
    normal: StringProperty(
        name='Normal',
        default='normal nor nrm nrml norm',)
        
    bump: StringProperty(
        name='Bump',
        default='bump bmp',)
        
    rough: StringProperty(
        name='Roughness',
        default='roughness rough rgh',)
        
    gloss: StringProperty(
        name='Gloss',
        default='gloss glossy glossiness',)
        
    displacement: StringProperty(
        name='Displacement',
        default='displacement displace disp dsp height heightmap',)
        
    transmission: StringProperty(
        name='Transmission',
        default='transmission transparency',)
        
    emission: StringProperty(
        name='Emission',
        default='emission emissive emit',)
        
    alpha: StringProperty(
        name='Alpha',
        default='alpha opacity',)
        
    ao: StringProperty(
        name='Ambient Occlusion',
        default='ao ambient occlusion occ',)
        
    displacement: StringProperty(
        name='Displacement',
        default='disp displacement',)
        
    delete_before_build: BoolProperty(
        name="Delete Nodes Before Build",
        description="When enabled, this will delete previously existing nodes for your active material while building",
        default=False
    )
    
    debug_mode: BoolProperty(
        name="Debug Mode",
        description="When enabled, debugging information will be printed onto the System Console",
        default=False
    )

def dprint(text):
    if bpy.context.scene.RMB.debug_mode:
        print('\x1b[7;36;40m' + '[RMB]' + '\x1b[0m ' + text)

def rsEnabled():
    for addon in bpy.context.preferences.addons:
        if addon.module == "redshift":
            return True
    return False

def updateList():
    """Updates texture list which filters based on image type and user-specified filter. This should only be called after a filter or target folder change"""
    props = bpy.context.scene.RMB
    
    for i, c in enumerate(material_dir_group):
        setattr(props, material_dir_group[i], "")
    
    if props.base_dir:
        image_files = [".bmp", ".jpg", ".jpeg", ".png", ".tga", ".exr", ".hdr", ".tif", ".tiff", ".webp"] # Only read files with these extensions
        if os.path.isdir(bpy.path.abspath(props.base_dir)):
            for i, textures in enumerate(os.listdir(bpy.path.abspath(props.base_dir))):
                if (textures.endswith(tuple(image_files))):

                    # Loop match thru each possible texture type
                    for i, mat in enumerate(material_group):
                        matcher = getattr(props, mat)
                        queries = matcher.split()
                        
                        for q in queries:
                            if search(q, textures, IGNORECASE):
                                if props.file_filter: # Filter query, if any is used
                                    for word in props.file_filter.split():
                                        if search(word, textures, IGNORECASE):
                                            file = bpy.path.abspath(str(props.base_dir) + textures)
                                            setattr(props, material_dir_group[i],file)
                                            break
                                else:
                                    file = bpy.path.abspath(str(props.base_dir) + textures)
                                    setattr(props, material_dir_group[i],file)
                                break
    return None
    
class RMB_guess(bpy.types.Operator):
    """Determines appropraite texture types by user-specified key words"""
    bl_label = "Set by Keywords"
    bl_idname = "node.rmb_guess"

    def execute(self, context):
        props = bpy.context.scene.RMB
        global image_node_matches
        image_node_matches = []
        
        for node in bpy.context.active_object.active_material.node_tree.nodes:
            if node.bl_idname == "ShaderNodeTexImage":
                if node.image:
                    # Loop match thru each possible texture type
                    for i, mat in enumerate(material_group):
                        matcher = getattr(props, mat)
                        queries = matcher.split()
                    
                        for q in queries:
                            texture = bpy.path.basename(node.image.filepath)
                            if search(q, texture, IGNORECASE):
                                setattr(node.image, "texture_type", mat)
                                dprint("Matched: "+str(node.image.name))
                                image_node_matches.append(node.image.name)
                            else:
                                if node.image.name in image_node_matches:
                                    break
                                continue
                            break
                        
        return {"FINISHED"}

def create_node(id, x=0, y=0):
    """Creates a node for the active material, where id represents the bl_idname of the node to be created."""
    
    dprint("Creating "+ str(id) + "...")
    mat = bpy.context.active_object.active_material
    nodes = mat.node_tree.nodes
    node = nodes.new(id)
    node.location = (x,y)
    
    if id == "rsTextureSamplerShaderNode":
        node.inputs[6].default_value = bpy.context.scene.RMB.uv_map # Set active UV Map for all samplers
    return node
    
def link_node(from_input, to_output):
    """Links a node output into a node input for active material."""
    mat = bpy.context.active_object.active_material
    mat.node_tree.links.new(from_input, to_output)
    
def load_file(path):
    """Loads an image file. If it's already used in the blender file, use it instead of loading it again."""
    props = bpy.context.scene.RMB
    
    for image in bpy.data.images:
        if bpy.path.abspath(image.filepath) == path:
            dprint("Texture " + str(image.name) + " already loaded in file. Using it instead...")
            if props.use_udim:
                dprint("Switching texture to UDIM")
                image.source = "TILED"
            return image
        
    tex = bpy.data.images.load(path)
    if props.use_udim:
        dprint("Setting texture to UDIM")
        tex.source = "TILED"
    dprint("Loaded texture " + str(path))
    return tex
    
class RMB_build(bpy.types.Operator):
    """Builds a Redshift Standard Material based on the textures specified by the user"""
    bl_label = "Build"
    bl_idname = "node.rmb_build"
    
    def execute(self, context):
        props = bpy.context.scene.RMB

        if not props.uv_map in bpy.context.active_object.data.uv_layers:
            props.uv_map = bpy.context.active_object.data.uv_layers.active.name
            
        # material_dir_group = "dir_color","dir_ao","dir_metallic","dir_specular","dir_gloss","dir_rough","dir_transmission","dir_sss","dir_normal","dir_bump","dir_emission","dir_alpha", "dir_displacement"
        build_material(tex_base_color=props.dir_color,tex_ao=props.dir_ao,tex_metallic=props.dir_metallic,tex_specular=props.dir_specular,tex_gloss=props.dir_gloss,tex_rough=props.dir_rough,tex_transmission=props.dir_transmission,tex_sss=props.dir_sss,tex_normal=props.dir_normal,tex_bump=props.dir_bump,tex_emission=props.dir_emission,tex_alpha=props.dir_alpha,tex_displacement=props.dir_displacement)
        return({"FINISHED"})
    
class RMB_from_nodes(bpy.types.Operator):
    """Builds a Redshift Standard Material based on the textures currently supplied from the active material via Image Texture nodes"""
    bl_label = "Build"
    bl_idname = "node.rmb_from_nodes"
    
    def execute(self, context):
        # Initialize texture array. [0] is type where [1] is file path
        possible_textures = []
        for t in material_group:
            possible_textures.append((t,None))
        
        dprint(f"Scanning through possible image nodes...")
        for node in bpy.context.active_object.active_material.node_tree.nodes:
            if node.bl_idname == "ShaderNodeTexImage":
                if node.image:
                    for i,e in enumerate(possible_textures):
                        if possible_textures[i][0] == node.image.texture_type:
                            possible_textures[i] = (possible_textures[i][0], bpy.path.abspath(node.image.filepath))
                
        possible_textures = tuple(possible_textures)
        dprint(f"Textures to build from: {possible_textures}")
        # material_dir_group = "dir_color","dir_ao","dir_metallic","dir_specular","dir_gloss","dir_rough","dir_transmission","dir_sss","dir_normal","dir_bump","dir_emission","dir_alpha", "dir_displacement"
        build_material(tex_base_color=possible_textures[0][1],tex_ao=possible_textures[1][1],tex_metallic=possible_textures[2][1],tex_specular=possible_textures[3][1],tex_gloss=possible_textures[4][1],tex_rough=possible_textures[5][1],tex_transmission=possible_textures[6][1],tex_sss=possible_textures[7][1],tex_normal=possible_textures[8][1],tex_bump=possible_textures[9][1],tex_emission=possible_textures[10][1],tex_alpha=possible_textures[11][1],tex_displacement=possible_textures[12][1])
        return({"FINISHED"})

def build_material(tex_base_color=None,tex_ao=None,tex_metallic=None,tex_specular=None,tex_gloss=None,tex_rough=None,tex_transmission=None,tex_sss=None,tex_normal=None,tex_bump=None,tex_emission=None,tex_alpha=None,tex_displacement=None):
    origin = [0,0]
    mat = bpy.context.active_object.active_material
    mat.use_nodes = True
    
    props = bpy.context.scene.RMB
    
    # DELETE ALL NODES
    if props.delete_before_build:
        bpy.ops.node.select_all(action='SELECT')
        bpy.ops.node.delete()
    else:
        bpy.ops.node.select_all(action='DESELECT')
    
    # CREATE STANDARD MATERIAL
    rsMaterial = create_node("rsStandardMaterialShaderNode", origin[0], origin[1])
    
    # CREATE VECTOR SCALE
    if props.scalar_node:
        dprint("Creating Standard Material...")
        matVector = create_node("rsRSVectorMakerShaderNode", origin[0]-1600, origin[1])
        
        matVector.inputs[0].default_value = 1
        matVector.inputs[1].default_value = 1
    
    # CREATE BASE COLOR
    coloffset = 400
    if tex_base_color:
        
        if props.correct_node:
            color_correct = create_node('rsRSColorCorrectionShaderNode', origin[0]-coloffset, origin[1])
            coloffset +=400
            
        rsMaterial.inputs[1].default_value = False # Open RS Base Dropdown
        base_color = create_node('rsTextureSamplerShaderNode', origin[0]-coloffset, origin[1])
        
        tex = load_file(bpy.path.abspath(tex_base_color)) # Load texture to file
        tex.colorspace_settings.name = props.color_space
        
        if props.image_node:
            viewport_node = create_node('ShaderNodeTexImage', origin[0]-coloffset-1600, origin[1])
            viewport_node.image = tex

        origin[1] -= 400  # Offsets y-axis for the next node to be placed next to it
        base_color.inputs[2].default_value = tex # Set file to node
        base_color.inputs[0].default_value = False # Expand General Dropdown
        base_color.label = "Base Color"
        if props.correct_node:
            
            link_node(base_color.outputs[0], color_correct.inputs[0])
            link_node(color_correct.outputs[0], rsMaterial.inputs[2])
        else:
            link_node(base_color.outputs[0], rsMaterial.inputs[2])
        
        if props.scalar_node:
            link_node(matVector.outputs[0], base_color.inputs[12])
        
    # CREATE AO
    if tex_ao:
        rsMaterial.inputs[1].default_value = False # Open RS Base Dropdown
        offset = -400
        
        ao = create_node('rsTextureSamplerShaderNode', origin[0]-coloffset, origin[1]+400)
        tex = load_file(bpy.path.abspath(tex_ao))
        tex.colorspace_settings.name = 'Non-Color'
        ao.inputs[2].default_value = tex # Set file to node
        ao.inputs[0].default_value = False # Expand General Dropdown
        ao.label = "AO"
        
        if base_color:
            ao.location = (ao.location[0]-400, ao.location[1])
            base_color.inputs[15].default_value = False # Opens "Adjust" dropdown for Base Color node

            link_node(ao.outputs[0], base_color.inputs[16]) # Connect to Base Color Multiplier
        else: # Use AO as a base color instead
            link_node(ao.outputs[0], rsMaterial.inputs[2]) # Connect to Standard Material Base Color
            tex.colorspace_settings.name = props.color_space # Change space
            
        if props.scalar_node:
            link_node(matVector.outputs[0], ao.inputs[12])
            
    # CREATE METALLIC
    if tex_metallic:
        rsMaterial.inputs[1].default_value = False # Open RS Base Dropdown
        metalness = create_node('rsTextureSamplerShaderNode', origin[0]-400, origin[1])
        origin[1] -= 300
        
        tex = load_file(bpy.path.abspath(tex_metallic)) # Load texture to file
        tex.colorspace_settings.name = 'Non-Color'
        metalness.inputs[2].default_value = tex # Set file to node
        metalness.inputs[0].default_value = False # Expand General Dropdown
        metalness.label = "Metalness" # Label the node
        link_node(metalness.outputs[0], rsMaterial.inputs[6]) # Connect nodes
        
        if props.scalar_node:
            link_node(matVector.outputs[0], metalness.inputs[12])
        
    # CREATE SPECULAR
    if tex_specular:
        rsMaterial.inputs[7].default_value = False # Open RS Reflection Dropdown
        specular = create_node('rsTextureSamplerShaderNode', origin[0]-400, origin[1])
        origin[1] -= 300
        
        tex = load_file(bpy.path.abspath(tex_specular)) # Load texture to file
        tex.colorspace_settings.name = 'Non-Color'
        specular.inputs[2].default_value = tex # Set file to node
        specular.inputs[0].default_value = False # Expand General Dropdown
        specular.label = "Specular"
        link_node(specular.outputs[0], rsMaterial.inputs[8])
        
        if props.scalar_node:
            link_node(matVector.outputs[0], specular.inputs[12])
        
    # CREATE GLOSS
    if tex_gloss and not tex_rough: # Gloss and rough maps cannot be used at the same time. If a rough map is supplied, roughness will be used instead.
        rsMaterial.inputs[7].default_value = False # Open RS Reflection Dropdown
        gloss_invert = create_node('rsRSMathInvColorShaderNode', origin[0]-400, origin[1])
        gloss = create_node('rsTextureSamplerShaderNode', origin[0]-800, origin[1])
        origin[1] -= 300
        
        tex = load_file(bpy.path.abspath(tex_gloss))
        tex.colorspace_settings.name = 'Non-Color'
        gloss.inputs[2].default_value = tex
        gloss.inputs[0].default_value = False # Expand General Dropdown
        gloss.label = "Gloss"
        link_node(gloss_invert.outputs[0], rsMaterial.inputs[10])
        link_node(gloss.outputs[0], gloss_invert.inputs[0])
        
        if props.scalar_node:
            link_node(matVector.outputs[0], gloss.inputs[12])
        
    # CREATE ROUGH
    if tex_rough:
        rsMaterial.inputs[7].default_value = False # Open RS Reflection Dropdown
        rough = create_node('rsTextureSamplerShaderNode', origin[0]-400, origin[1])
        origin[1] -= 300
        
        tex = load_file(bpy.path.abspath(tex_rough))
        tex.colorspace_settings.name = 'Non-Color'
        rough.inputs[2].default_value = tex
        rough.inputs[0].default_value = False # Expand General Dropdown
        rough.label = "Roughness"
        link_node(rough.outputs[0], rsMaterial.inputs[10])
        
        if props.scalar_node:
            link_node(matVector.outputs[0], rough.inputs[12])
        
    # CREATE TRANSMISSION
    if tex_transmission:
        rsMaterial.inputs[15].default_value = False # Open RS Transmission Dropdown
        transmission = create_node('rsTextureSamplerShaderNode', origin[0]-400, origin[1])
        origin[1] -= 300
        
        tex = load_file(bpy.path.abspath(tex_transmission))
        tex.colorspace_settings.name = 'Non-Color' 
        transmission.inputs[2].default_value = tex
        transmission.inputs[0].default_value = False # Expand General Dropdown
        transmission.label = "Transmission"
        link_node(transmission.outputs[0], rsMaterial.inputs[17])
        
        if props.scalar_node:
            link_node(matVector.outputs[0], transmission.inputs[12])
        
    # CREATE SSS
    if tex_sss:
        rsMaterial.inputs[25].default_value = False # Open RS Subsurface Dropdown
        sss = create_node('rsTextureSamplerShaderNode', origin[0]-400, origin[1])
        origin[1] -= 300
        
        tex = load_file(bpy.path.abspath(tex_sss))
        tex.colorspace_settings.name = 'Non-Color'
        sss.inputs[2].default_value = tex
        sss.inputs[0].default_value = False # Expand General Dropdown
        sss.label = "SSS"
        if int(props.sss_map_input) == 0 or int(props.sss_map_input) == 2:
            dprint("Linking SSS Weight")
            link_node(sss.outputs[0], rsMaterial.inputs[27]) # Weight
        if int(props.sss_map_input) >= 1:
            dprint("Linking SSS Color")
            link_node(sss.outputs[0], rsMaterial.inputs[26]) # Color
            rsMaterial.inputs[27].default_value = 1.0

        
        if props.scalar_node:
            link_node(matVector.outputs[0], sss.inputs[12])
        
    # CREATE NORMAL
    if tex_normal:
        bpy.context.active_object.redshift.skipTangents = True if props.normal_type == "2" else False
        rsMaterial.inputs[54].default_value = False # Open RS Geometry Dropdown
        rs_nbump = create_node('rsBumpMapShaderNode', origin[0]-400, origin[1])
        normal = create_node('rsTextureSamplerShaderNode', origin[0]-800, origin[1])
        origin[1] -= 300

        rs_nbump.inputs[9].default_value = 1.0
        rs_nbump.inputs[4].default_value = props.normal_scale
        
        tex = load_file(bpy.path.abspath(tex_normal))
        tex.colorspace_settings.name = 'Non-Color'
        normal.inputs[2].default_value = tex
        normal.inputs[0].default_value = False # Expand General Dropdown
        normal.label = "Normal"
        
        rs_nbump.inputs[2].default_value = props.normal_type
        
        link_node(rs_nbump.outputs[0], rsMaterial.inputs[57])
        link_node(normal.outputs[0], rs_nbump.inputs[3])
        
        if props.scalar_node:
            link_node(matVector.outputs[0], normal.inputs[12])
        
    # CREATE BUMP
    if tex_bump:
        rsMaterial.inputs[54].default_value = False # Open RS Geometry Dropdown
        rs_bump = create_node('rsBumpMapShaderNode', origin[0]-400, origin[1])
        bump = create_node('rsTextureSamplerShaderNode', origin[0]-800, origin[1])
        
        tex = load_file(bpy.path.abspath(tex_bump))
        tex.colorspace_settings.name = 'Non-Color'
        bump.inputs[2].default_value = tex
        bump.inputs[0].default_value = False # Expand General Dropdown
        bump.label = "Bump"
        
        rs_bump.inputs[4].default_value = props.bump_scale
        
        if tex_normal:
            bump_blender = create_node('rsBumpBlenderShaderNode', origin[0], origin[1])
            bump_blender.inputs[4].default_value = 1 # Blend Weight Layer 0
            bump_blender.inputs[11].default_value = True # Additive Mode
            
            link_node(bump.outputs[0], rs_bump.inputs[3])
            link_node(rs_bump.outputs[0], bump_blender.inputs[3]) # Bump to Layer 0
            link_node(rs_nbump.outputs[0], bump_blender.inputs[1]) # Normal to Input
            link_node(bump_blender.outputs[0], rsMaterial.inputs[57]) # BumpBlender to Standard
        else:
            link_node(rs_bump.outputs[0], rsMaterial.inputs[57])
            link_node(bump.outputs[0], rs_bump.inputs[3])
            
        if props.scalar_node:
            link_node(matVector.outputs[0], bump.inputs[12])
    
        origin[1] -= 300
        
    # CREATE ALPHA
    rsOutput = create_node('RedshiftMaterialOutputNode', origin[0]+400, 0)
        
    if tex_alpha or props.color_is_alpha:
        alpha = create_node('rsSpriteShaderNode', origin[0]+300, 0)
        
        if props.color_is_alpha:
            tex = load_file(bpy.path.abspath(tex_base_color))
            alpha.inputs[3].default_value = tex
        else:
            tex = load_file(bpy.path.abspath(tex_alpha))
            alpha.inputs[3].default_value = tex

        alpha.inputs[2].default_value = False # Expand Stencil Dropdown
        alpha.label = "Alpha"
        rsOutput.location[0] += 200
        alpha.inputs[4].default_value = props.uv_map

        if props.color_is_alpha:
            alpha.inputs[5].default_value = '1'
        else:
            alpha.inputs[5].default_value = props.alpha_type
        
        link_node(rsMaterial.outputs[0], alpha.inputs[1])
        link_node(alpha.outputs[0], rsOutput.inputs[0])
    else:
        link_node(rsMaterial.outputs[0], rsOutput.inputs[0])

    # CREATE EMISSION
    if tex_emission:
        rsMaterial.inputs[51].default_value = False # Open RS Emission Dropdown
        emission = create_node('rsTextureSamplerShaderNode', origin[0]-400, origin[1])
        origin[1] -= 300
        
        tex = load_file(bpy.path.abspath(tex_emission))
        tex.colorspace_settings.name = 'Non-Color'
        emission.inputs[2].default_value = tex
        emission.inputs[0].default_value = False # Expand General Dropdown
        emission.label = "Emission"
        link_node(emission.outputs[0], rsMaterial.inputs[52])
        rsMaterial.inputs[53].default_value = 1.0
        
        if props.scalar_node:
            link_node(matVector.outputs[0], emission.inputs[12])
        
    rsMaterial.location[1] = origin[1]*0.25

    # CREATE DISPLACEMENT
    if tex_displacement:
        rsMaterial.inputs[54].default_value = False # Open RS Geometry Dropdown
        rs_disp = create_node('rsDisplacementShaderNode', origin[0], origin[1])
        displacement = create_node('rsTextureSamplerShaderNode', origin[0]-400, origin[1])
        origin[1] -= 300
        
        tex = load_file(bpy.path.abspath(tex_displacement))
        tex.colorspace_settings.name = 'Non-Color'
        displacement.inputs[2].default_value = tex
        displacement.inputs[0].default_value = False
        displacement.label = "Displacement"
        
        rs_disp.inputs[10].default_value = -1.0 # New Range Min
        rs_disp.inputs[6].default_value = props.uv_map
        bpy.context.active_object.rsTessDisp.GetTessellationEnabled = True
        bpy.context.active_object.rsTessDisp.GetDisplacementEnabled = True
        bpy.context.active_object.rsTessDisp.GetDisplacementScale = 1.0 # As of 3515 displacement wont show in the IPR unless its value is changed again. This is an attempt at fixing the problem
        rs_disp.inputs[2].default_value = props.displacement_scale # Set displacement scale from user input
        
        if props.normal_type == "1":
            rs_disp.inputs[4].default_value = "2"
        
        link_node(rs_disp.outputs[0], rsOutput.inputs[1])
        link_node(displacement.outputs[0], rs_disp.inputs[1])
        
        if props.scalar_node:
            link_node(matVector.outputs[0], displacement.inputs[12])

    bpy.ops.object.editmode_toggle()
    bpy.ops.object.editmode_toggle() # 3602: For some reason Redshift will not show IPR normals/displacement on newly-built materials until the object goes thru Edit Mode atleast once(???)

    dprint("---- BUILD COMPLETE ----")

class FileSelector(ImportHelper):
    filepath : StringProperty(
        name="File Path",
        description="Filepath used for importing the file",
        maxlen=1024,
        default="")

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
class RMB_OT_LoadDirectory(bpy.types.Operator, FileSelector):
    bl_idname = "rmb.load_texture"
    bl_label = "Load Texture File"
    bl_description = "Load texture from file"
    bl_options = {'UNDO'}

    texture_target : StringProperty()
    
    def execute(self, context):
        setattr(bpy.context.scene.RMB, self.texture_target, self.filepath)
        dprint(self.filepath + " was set for texture type " + str(self.texture_target))
        return {'FINISHED'}

    def invoke(self, context, event):
        scene = bpy.context.scene
        self.properties.filepath = scene.RMB.base_dir
        dprint("Invoking file explorer, the path to load to is "+str(os.path.dirname(scene.RMB.base_dir)))
        return FileSelector.invoke(self, context, event)
      
class RMBpanel_create(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Build from Files"
    bl_idname = "NODE_PT_rmb_create"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "RMB"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        if space.node_tree is not None and space.node_tree.library is None and space.tree_type == "ShaderNodeTree":
            return True
        return False
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="",icon="IMAGE_DATA")
        
    def draw(self, context):
        
        layout = self.layout
        scene = context.scene
        
        if not rsEnabled():
            layout.label(text="Redshift is not enabled", icon="ERROR")
            
        else:
            props = scene.RMB
            layout.prop(props, "base_dir")
            layout.prop(props, "file_filter", text="", icon="FILTER")
            layout.separator()
            row = layout.row()
            row.scale_y = 1.5
            row.operator("node.rmb_build")
            
            v = False
            for prop in material_dir_group:
                if getattr(props, prop):
                    v = True
                    break
            
            if not v: 
                row.enabled = False
                layout.label(text="Specify at least one texture", icon="ERROR")

            if len(bpy.context.active_object.data.uv_layers) == 0:
                row.enabled = False
                layout.label(text="No UV maps exist on this object", icon="ERROR")
            elif not props.uv_map in bpy.context.active_object.data.uv_layers:
                layout.label(text="Selected UV Map does not exist, using active instead", icon="INFO")

            if getattr(context.scene.RMB, material_dir_group[4]) and getattr(context.scene.RMB, material_dir_group[5]):
                layout.label(text="Roughness will take precedence over Gloss", icon="INFO")
    
            layout.separator()

            for prop in material_dir_group:
                    row = layout.row()
                    row.prop(props, prop)
                    row.operator("rmb.load_texture",text="",icon="FILE_FOLDER").texture_target = str(prop)

class RMBpanel_from_nodes(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Build from Nodes"
    bl_idname = "NODE_PT_rmb_from_nodes"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "RMB"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        if space.node_tree is not None and space.node_tree.library is None and space.tree_type == "ShaderNodeTree":
            return True
        return False
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="",icon="NODE_SEL")
        
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        if not rsEnabled():
            layout.label(text="Redshift is not enabled", icon="ERROR")
            
        else:
            global image_node_matches
            props = scene.RMB
            
            #####
            v = False
            count = 0
            convert_items = []
            brow = layout.row()
            brow.scale_y = 1.5
            brow.operator("node.rmb_from_nodes")
            erres = layout.column()
            layout.separator()
            grow = layout.row()
            nomatch = layout.row()
            for node in bpy.context.active_object.active_material.node_tree.nodes:
                if node.bl_idname == "ShaderNodeTexImage":
                    if node.image:
                        
                        n = []
                        for k in convert_items:
                            n.append(k[0])

                        if node.image.filepath not in n:
                            convert_items.append((node.image.filepath, node.image.texture_type))
                            count += 1
                            row = layout.row()
                            if node.image.name in image_node_matches:
                                row.label(text=bpy.path.basename(node.image.filepath), icon="OUTLINER_OB_IMAGE")
                            else:
                                row.label(text=bpy.path.basename(node.image.filepath), icon="IMAGE_DATA")
                            
                            row.prop(node.image, "texture_type", text="")
                            v = True
                        
            if v:
                grow.operator("node.rmb_guess")
            
            w = False
            to = []
            for item in convert_items:
                to.append(item[1])

            for type in material_group:
                if str(to).count(type) >= 2:
                    w = True
                    break

            if w:
                brow.enabled = False
                erres.label(text="All image nodes must have a unique texture type", icon="ERROR")
                
            if not v: 
                brow.enabled = False
                erres.label(text="Requires one valid Image Node texture", icon="ERROR")

            if len(bpy.context.active_object.data.uv_layers) == 0:
                brow.enabled = False
                erres.label(text="No UV maps exist on this object", icon="ERROR")
            elif not props.uv_map in bpy.context.active_object.data.uv_layers:
                erres.label(text="Selected UV Map does not exist, using active instead", icon="INFO")
            
            g = False
            r = False
            for node in bpy.context.active_object.active_material.node_tree.nodes:
                if node.bl_idname == "ShaderNodeTexImage":
                    if node.image.texture_type == "gloss":
                        g = True
                    if node.image.texture_type == "rough":
                        r = True
            
            if r and g:
                erres.label(text="Roughness will take precedence of Gloss", icon="INFO")
            
class RMBpanel_settings(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Settings"
    bl_idname = "NODE_PT_rmb_settings"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "RMB"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        if space.node_tree is not None and space.node_tree.library is None and space.tree_type == "ShaderNodeTree":
            return True
        return False
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="",icon="SETTINGS")
        
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        if not rsEnabled():
            layout.label(text="Redshift is not enabled",icon="ERROR")
        else:
            props = scene.RMB
            
            nodebox = layout.box()
            nodebox.label(text="Node", icon="NODE")
            nodebox.prop(props,"scalar_node")
            nodebox.prop(props,"image_node")
            nodebox.prop(props,"correct_node")
            nodebox.separator(factor=0.5)
            nodebox.prop(props,"delete_before_build")
            
            layout.separator(factor=0.3)

            uvbox = layout.box()
            uvrow = uvbox.row()
            uvleft = uvrow.split()
            uvleft.scale_x = 0.9
            uvleft.label(text="UV", icon='GROUP_UVS')
            uvrow.prop_search(scene.RMB, "uv_map", context.object.data, "uv_layers", text="",icon="BLANK1")
            uvrow.prop(props,"use_udim",text="UDIM")
            
            layout.separator(factor=0.3)
            
            inputbox = layout.box()
            inputbox.label(text="Texture",icon="TEXTURE")
            colrow = inputbox.row()
            colrow.prop(props,"color_space",text="Diffuse")
            colrow.prop(props,"color_is_alpha")
            inputbox.prop(props,"normal_type",text="Normal")
            inputbox.prop(props,"sss_map_input",text="SSS")
            inputbox.prop(props,"alpha_type",text="Alpha")
            
            layout.separator(factor=0.3)

            scalebox = layout.box()
            scalebox.label(text="Scale",icon="FULLSCREEN_ENTER")
            scaleheader = scalebox.row()
            scaleheader.label(text="Normal")
            scaleheader.label(text="Bump")
            scaleheader.label(text="Displacement")
            scalerow = scalebox.row()
            scalerow.prop(props,"normal_scale",text="")
            scalerow.prop(props,"bump_scale",text="")
            scalerow.prop(props,"displacement_scale",text="")
            
            layout.separator(factor=0.3)
            
            keybox = layout.box()
            keybox.label(text="Keywords",icon="TEXT")
            keybox.prop(props, "base_color")
            keybox.prop(props, "ao")
            keybox.prop(props, "metallic")
            keybox.prop(props, "specular")
            keybox.prop(props, "gloss")
            keybox.prop(props, "rough")
            keybox.prop(props, "transmission")
            keybox.prop(props, "sss")
            keybox.prop(props, "normal")
            keybox.prop(props, "bump")
            keybox.prop(props, "emission")
            keybox.prop(props, "alpha")
            keybox.prop(props, "displacement")
            
            layout.separator(factor=5)
            
            layout.prop(props, "debug_mode")
            
classes = (RMBpanel_create,RMBpanel_from_nodes,RMBpanel_settings,RMB_props,RMB_build,RMB_from_nodes,RMB_guess,RMB_OT_LoadDirectory)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.RMB = bpy.props.PointerProperty(type=RMB_props)

    mat_items = []
    for i,item in enumerate(material_group):
        display = item
        
        if display == "base_color":
            display = "Base Color"
        elif display == "sss":
            display = "SSS"
        elif display == "ao":
            display = "AO"
        else:
            display = display.capitalize()
        mat_items.append((item, display,"", i))
        
    mat_items.append(("ignore", "Ignore", "Textures marked as ignored will not be used in the built material", "PANEL_CLOSE", len(mat_items)))
        
    bpy.types.Image.texture_type = bpy.props.EnumProperty(
        name="Texture Type",
        description="The type of texture used for this setup",
        items =  mat_items,
        default = 0
    )

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    del bpy.types.Scene.RMB
    del bpy.types.Image.texture_type
    del bpy.types.Image.texture_bool

if __name__ == "__main__":
    register()
