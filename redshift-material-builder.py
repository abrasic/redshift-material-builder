import bpy, os
from re import (search, IGNORECASE)

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
    "version": (1, 0),
    "blender": (3, 5, 0),
    "location": "Shader Editor > N-Panel > RMB",
    "support": "COMMUNITY",
    "category": "Node",
}

material_group = ["base_color","ao","metallic","specular","gloss","rough","transmission","sss","normal","bump","emission","alpha", "displacement"]
material_dir_group = ["dir_color","dir_ao","dir_metallic","dir_specular","dir_gloss","dir_rough","dir_transmission","dir_sss","dir_normal","dir_bump","dir_emission","dir_alpha", "dir_displacement"]

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
        default="",
        subtype = "FILE_PATH")  
        
    dir_ao: StringProperty (
        name="AO",
        description="",
        default="",
        subtype = "FILE_PATH")  
        
    dir_metallic: StringProperty (
        name="Metallic",
        description="",
        default="",
        subtype = "FILE_PATH")  
        
    dir_specular: StringProperty (
        name="Specular",
        description="",
        default="",
        subtype = "FILE_PATH")  
        
    dir_gloss: StringProperty (
        name="Gloss",
        description="",
        default="",
        subtype = "FILE_PATH")  
        
    dir_rough: StringProperty (
        name="Roughness",
        description="",
        default="",
        subtype = "FILE_PATH")  
        
    dir_transmission: StringProperty (
        name="Transmission",
        description="",
        default="",
        subtype = "FILE_PATH")  
        
    dir_sss: StringProperty (
        name="SSS",
        description="",
        default="",
        subtype = "FILE_PATH")  
        
    dir_normal: StringProperty (
        name="Normal",
        description="",
        default="",
        subtype = "FILE_PATH")  

    dir_bump: StringProperty (
        name="Bump",
        description="",
        default="",
        subtype = "FILE_PATH")  

    dir_emission: StringProperty (
        name="Emission",
        description="",
        default="",
        subtype = "FILE_PATH")  

    dir_alpha: StringProperty (
        name="Alpha",
        description="",
        default="",
        subtype = "FILE_PATH")   
        
    dir_displacement: StringProperty (
        name="Displacement",
        description="",
        default="",
        subtype = "FILE_PATH")   
        
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
        default=True
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
    
    normal_flip: BoolProperty(
        name="Flip Normal Scale",
        description="-1 will be used for normal scale instead of 1",
        default=False
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

def dprint(text):
    print('\x1b[7;36;40m' + '[RMB]' + '\x1b[0m ' + text)

def rsEnabled():
    for addon in bpy.context.preferences.addons:
        if addon.module == "redshift":
            return True
    return False

def updateList():
    props = bpy.context.scene.RMB
    
    for i,c in enumerate(material_dir_group):
        setattr(props, material_dir_group[i], "")
    
    if props.base_dir:
        image_files = [".bmp", ".jpg", ".jpeg", ".png", ".tga", ".exr", ".hdr", ".tif", ".tiff", ".webp"] # Only read files with these extensions
        if os.path.isdir(bpy.path.abspath(props.base_dir)):
            for i, textures in enumerate(os.listdir(bpy.path.abspath(props.base_dir))):
                if (textures.endswith(tuple(image_files))):

                    # Loop match thru each material group
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
    for image in bpy.data.images:
        if bpy.path.abspath(image.filepath) == path:
            dprint("Texture " + str(image.name) + " already loaded in file. Using it instead...")
            return image
        
    tex = bpy.data.images.load(path)
    dprint("Texture " + str(path) + "loaded")
    return tex
    
class RMB_build(bpy.types.Operator):
    """Builds a Redshift Standard Material based on the textures currently supplied"""
    bl_label = "Build"
    bl_idname = "node.rmb_build"

    def execute(self, context):
        origin = [0,0]
        mat = bpy.context.active_object.active_material
        mat.use_nodes = True
        
        props = context.scene.RMB
        
        # DELETE ALL NODES
        if props.delete_before_build:
            bpy.ops.node.select_all(action='SELECT')
            bpy.ops.node.delete()

        
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
        if props.dir_color:
            
            if props.correct_node:
                color_correct = create_node('rsRSColorCorrectionShaderNode', origin[0]-coloffset, origin[1])
                coloffset +=400
                
            rsMaterial.inputs[1].default_value = False # Open RS Base Dropdown
            base_color = create_node('rsTextureSamplerShaderNode', origin[0]-coloffset, origin[1])
            
            tex = load_file(bpy.path.abspath(props.dir_color)) # Load texture to file
            tex.colorspace_settings.name = 'sRGB'
            
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
        if props.dir_ao:
            rsMaterial.inputs[1].default_value = False # Open RS Base Dropdown
            offset = -400
            
            ao = create_node('rsTextureSamplerShaderNode', origin[0]-coloffset, origin[1]+400)
            tex = load_file(bpy.path.abspath(props.dir_ao))
            tex.colorspace_settings.name = 'Raw'
            ao.inputs[2].default_value = tex # Set file to node
            ao.inputs[0].default_value = False # Expand General Dropdown
            ao.label = "AO"
            
            if context.scene.RMB.dir_color:
                ao.location = (ao.location[0]-400, ao.location[1])
                base_color.inputs[15].default_value = False # Opens "Adjust" dropdown for Base Color node

                link_node(ao.outputs[0], base_color.inputs[16]) # Connect to Base Color Multiplier
            else: # Use AO as a base color instead
                link_node(ao.outputs[0], rsMaterial.inputs[2]) # Connect to Standard Metail Base Color
                tex.colorspace_settings.name = 'sRGB' # Change space
                
            if props.scalar_node:
                link_node(matVector.outputs[0], ao.inputs[12])
                
        # CREATE METALLIC
        if props.dir_metallic:
            rsMaterial.inputs[1].default_value = False # Open RS Base Dropdown
            metalness = create_node('rsTextureSamplerShaderNode', origin[0]-400, origin[1])
            origin[1] -= 300
            
            tex = load_file(bpy.path.abspath(props.dir_metallic)) # Load texture to file
            tex.colorspace_settings.name = 'Raw'
            metalness.inputs[2].default_value = tex # Set file to node
            metalness.inputs[0].default_value = False # Expand General Dropdown
            metalness.label = "Metalness" # Label the node
            link_node(metalness.outputs[0], rsMaterial.inputs[6]) # Connect nodes
            
            if props.scalar_node:
                link_node(matVector.outputs[0], metalness.inputs[12])
            
        # CREATE SPECULAR
        if props.dir_specular:
            rsMaterial.inputs[7].default_value = False # Open RS Reflection Dropdown
            specular = create_node('rsTextureSamplerShaderNode', origin[0]-400, origin[1])
            origin[1] -= 300
            
            tex = load_file(bpy.path.abspath(props.dir_specular)) # Load texture to file
            tex.colorspace_settings.name = 'Raw'
            specular.inputs[2].default_value = tex # Set file to node
            specular.inputs[0].default_value = False # Expand General Dropdown
            specular.label = "Specular"
            link_node(specular.outputs[0], rsMaterial.inputs[8])
            
            if props.scalar_node:
                link_node(matVector.outputs[0], specular.inputs[12])
            
        # CREATE GLOSS
        if props.dir_gloss and not props.dir_rough: # Gloss and rough maps cannot be used at the same time. If a rough map is supplied, roughness will be used instead.
            rsMaterial.inputs[7].default_value = False # Open RS Reflection Dropdown
            gloss_invert = create_node('rsRSMathInvColorShaderNode', origin[0]-400, origin[1])
            gloss = create_node('rsTextureSamplerShaderNode', origin[0]-800, origin[1])
            origin[1] -= 300
            
            tex = load_file(bpy.path.abspath(props.dir_gloss))
            tex.colorspace_settings.name = 'Raw'
            gloss.inputs[2].default_value = tex
            gloss.inputs[0].default_value = False # Expand General Dropdown
            gloss.label = "Gloss"
            link_node(gloss_invert.outputs[0], rsMaterial.inputs[10])
            link_node(gloss.outputs[0], gloss_invert.inputs[0])
            
            if props.scalar_node:
                link_node(matVector.outputs[0], gloss.inputs[12])
            
        # CREATE ROUGH
        if props.dir_rough:
            rsMaterial.inputs[7].default_value = False # Open RS Reflection Dropdown
            rough = create_node('rsTextureSamplerShaderNode', origin[0]-400, origin[1])
            origin[1] -= 300
            
            tex = load_file(bpy.path.abspath(props.dir_rough))
            tex.colorspace_settings.name = 'Raw'
            rough.inputs[2].default_value = tex
            rough.inputs[0].default_value = False # Expand General Dropdown
            rough.label = "Roughness"
            link_node(rough.outputs[0], rsMaterial.inputs[10])
            
            if props.scalar_node:
                link_node(matVector.outputs[0], rough.inputs[12])
            
        # CREATE TRANSMISSION
        if props.dir_transmission:
            rsMaterial.inputs[15].default_value = False # Open RS Transmission Dropdown
            transmission = create_node('rsTextureSamplerShaderNode', origin[0]-400, origin[1])
            origin[1] -= 300
            
            tex = load_file(bpy.path.abspath(props.dir_rough))
            tex.colorspace_settings.name = 'Raw' 
            transmission.inputs[2].default_value = tex
            transmission.inputs[0].default_value = False # Expand General Dropdown
            transmission.label = "Transmission"
            link_node(transmission.outputs[0], rsMaterial.inputs[17])
            
            if props.scalar_node:
                link_node(matVector.outputs[0], transmission.inputs[12])
            
        # CREATE SSS
        if props.dir_sss:
            rsMaterial.inputs[25].default_value = False # Open RS Subsurface Dropdown
            sss = create_node('rsTextureSamplerShaderNode', origin[0]-400, origin[1])
            origin[1] -= 300
            
            tex = load_file(bpy.path.abspath(props.dir_sss))
            tex.colorspace_settings.name = 'Raw'
            sss.inputs[2].default_value = tex
            sss.inputs[0].default_value = False # Expand General Dropdown
            sss.label = "SSS"
            link_node(sss.outputs[0], rsMaterial.inputs[27])
            
            if props.scalar_node:
                link_node(matVector.outputs[0], sss.inputs[12])
            
        # CREATE NORMAL
        if props.dir_normal:
            bpy.context.active_object.redshift.skipTangents = False
            bpy.ops.object.shade_smooth()
            rsMaterial.inputs[54].default_value = False # Open RS Geometry Dropdown
            rs_nbump = create_node('rsBumpMapShaderNode', origin[0]-400, origin[1])
            normal = create_node('rsTextureSamplerShaderNode', origin[0]-800, origin[1])
            origin[1] -= 300
            
            if props.normal_flip:
                rs_nbump.inputs[4].default_value = -1
            
            tex = load_file(bpy.path.abspath(props.dir_normal))
            tex.colorspace_settings.name = 'Raw'
            normal.inputs[2].default_value = tex
            normal.inputs[0].default_value = False # Expand General Dropdown
            normal.label = "Normal"
            
            rs_nbump.inputs[2].default_value = props.normal_type
            
            link_node(rs_nbump.outputs[0], rsMaterial.inputs[57])
            link_node(normal.outputs[0], rs_nbump.inputs[3])
            
            if props.scalar_node:
                link_node(matVector.outputs[0], normal.inputs[12])
            
        # CREATE BUMP
        if props.dir_bump:
            rsMaterial.inputs[54].default_value = False # Open RS Geometry Dropdown
            rs_bump = create_node('rsBumpMapShaderNode', origin[0]-400, origin[1])
            bump = create_node('rsTextureSamplerShaderNode', origin[0]-800, origin[1])
            
            tex = load_file(bpy.path.abspath(props.dir_normal))
            tex.colorspace_settings.name = 'Raw'
            bump.inputs[2].default_value = tex
            bump.inputs[0].default_value = False # Expand General Dropdown
            bump.label = "Bump"
            
            if props.dir_normal:
                bump_blender = create_node('rsBumpBlenderShaderNode', origin[0], origin[1])
                
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
            
        if props.dir_alpha:
            alpha = create_node('rsSpriteShaderNode', origin[0]+300, 0)
            
            tex = load_file(bpy.path.abspath(props.dir_alpha))
            alpha.inputs[3].default_value = tex
            alpha.inputs[2].default_value = False # Expand Stencil Dropdown
            alpha.label = "Alpha"
            link_node(alpha.outputs[0], rsMaterial.inputs[52])
            rsOutput.location[0] += 200
            alpha.inputs[5].default_value = props.alpha_type
            
            link_node(rsMaterial.outputs[0], alpha.inputs[1])
            link_node(alpha.outputs[0], rsOutput.inputs[0])
        else:
            link_node(rsMaterial.outputs[0], rsOutput.inputs[0])

        # CREATE EMISSION
        if props.dir_emission:
            rsMaterial.inputs[51].default_value = False # Open RS Emission Dropdown
            emission = create_node('rsTextureSamplerShaderNode', origin[0]-400, origin[1])
            origin[1] -= 300
            
            tex = load_file(bpy.path.abspath(props.dir_emission))
            tex.colorspace_settings.name = 'Raw'
            emission.inputs[2].default_value = tex
            emission.inputs[0].default_value = False # Expand General Dropdown
            emission.label = "Emission"
            link_node(emission.outputs[0], rsMaterial.inputs[52])
            rsMaterial.inputs[53].default_value = 1.0
            
            if props.scalar_node:
                link_node(matVector.outputs[0], emission.inputs[12])
            
        rsMaterial.location[1] = origin[1]*0.25
    
        # CREATE DISPLACEMENT
        if props.dir_displacement:
            rsMaterial.inputs[54].default_value = False # Open RS Geometry Dropdown
            rs_disp = create_node('rsDisplacementShaderNode', origin[0], origin[1])
            displacement = create_node('rsTextureSamplerShaderNode', origin[0]-400, origin[1])
            origin[1] -= 300
            
            tex = load_file(bpy.path.abspath(props.dir_displacement))
            tex.colorspace_settings.name = 'Raw'
            displacement.inputs[2].default_value = tex
            displacement.inputs[0].default_value = False
            displacement.label = "Displacement"
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
                
            dprint("Build Complete")
        return {"FINISHED"}
      
class RMBpanel_create(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Create"
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
        layout.label(text="",icon="ADD")
        
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
                row.enabled = False
            
            if not v: 
                layout.label(text="Specify at least one texture", icon="ERROR")

            if not props.uv_map in bpy.context.active_object.data.uv_layers:
                layout.label(text="Selected UV Map does not exist", icon="ERROR")
                row.enabled = False
            if getattr(context.scene.RMB, material_dir_group[4]) and getattr(context.scene.RMB, material_dir_group[5]):
                layout.label(text="Roughness will take precedence of Gloss", icon="INFO")
    
            layout.separator()

            for prop in material_dir_group:
                    layout.prop(props, prop)
            
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
            layout.prop(props,"scalar_node")
            layout.prop(props,"image_node")
            layout.prop(props,"correct_node")
            layout.prop(props,"normal_flip")
            layout.prop(props,"normal_type")
            layout.prop(props,"alpha_type")
            layout.prop_search(scene.RMB, "uv_map", context.object.data, "uv_layers", icon='GROUP_UVS')
            layout.prop(props,"displacement_scale")
            layout.prop(props,"delete_before_build")
            layout.separator(factor=1)
            layout.label(text="Texture Keywords:")
            layout.prop(props, "base_color")
            layout.prop(props, "ao")
            layout.prop(props, "metallic")
            layout.prop(props, "specular")
            layout.prop(props, "gloss")
            layout.prop(props, "rough")
            layout.prop(props, "transmission")
            layout.prop(props, "sss")
            layout.prop(props, "normal")
            layout.prop(props, "bump")
            layout.prop(props, "emission")
            layout.prop(props, "alpha")
            layout.prop(props, "displacement")
            
classes = (RMBpanel_create,RMBpanel_settings,RMB_props,RMB_build)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.RMB = bpy.props.PointerProperty(type=RMB_props)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    del bpy.types.Scene.RMB

if __name__ == "__main__":
    register()
