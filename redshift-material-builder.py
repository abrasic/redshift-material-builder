import bpy, os
from re import (search, IGNORECASE)

from bpy.props import (
    EnumProperty,
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
        name="Use Vector Scale",
        description="When enabled, a Vector input will be connected to all texture scales. This is useful for scaling all textures at once if you're using a PBR material",
        default=False
    )
    
    normal_type: EnumProperty(
        name="Normal Input",
        description="Sets the RS Bump node to this input type for its normal maps",
        items=[
                ('1', "Tangent-Space", "",),
                ('2', "Object-Space", ""),
               ]
    )
    
    alpha_type: EnumProperty(
        name="Alpha Input",
        description="Sets the Sprite node to this input type for its alpha maps",
        items=[
                ('0', "From Color Intensity", "",),
                ('1', "From Alpha", ""),
               ]
    )
    
    normal_flip: BoolProperty(
        name="Flip Scale",
        description="-1 will be used for height scale instead of 1",
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

def rsEnabled():
    for addon in bpy.context.preferences.addons:
        if addon.module == "redshift":
            return True
        
    return False

def updateList():
    props = bpy.context.scene.RMB
    
    for i,c in enumerate(material_dir_group):
        setattr(props, material_dir_group[i],"")
    
    image_files = [".bmp", ".jpg", ".jpeg", ".png", ".tga", ".exr", ".hdr", ".tif", ".tiff", ".webp"]
    if os.path.isdir(bpy.path.abspath(props.base_dir)):
        for i, textures in enumerate(os.listdir(bpy.path.abspath(props.base_dir))):
            if (textures.endswith(tuple(image_files))):

                # Loop match thru each material group
                for i, mat in enumerate(material_group):
                    matcher = getattr(props, mat)
                    queries = matcher.split()
                    
                    for q in queries:
                        if search(q, textures, IGNORECASE):
                            file = bpy.path.abspath(str(props.base_dir) + textures)
                            setattr(props, material_dir_group[i],file)
                            break
        return None
    
def create_node(id, x=0, y=0):
    """Creates a node for active material"""
    mat = bpy.context.active_object.active_material
    nodes = mat.node_tree.nodes
    node = nodes.new(id)
    node.location = (x,y)
    
    return node
    
def create_texture(path, colorspace, x, y, connect_scalar=False):
    create_node('TextureSampler')
    
def link_node(from_input, to_output):
    mat = bpy.context.active_object.active_material
    mat.node_tree.links.new(from_input, to_output)
    
def load_file(path):
    """Loads an image file. If it's already used in the blender file, use it instead of loading it again."""
    for image in bpy.data.images:
        if bpy.path.abspath(image.filepath) == path:
            return image
        
    tex = bpy.data.images.load(path)
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
        
        # CREATE STANDARD MATERIAL
        rsMaterial = create_node("rsStandardMaterialShaderNode", origin[0], origin[1])
        
        # CREATE VECTOR SCALE
        if props.scalar_node:
            matVector = create_node("rsRSVectorMakerShaderNode", origin[0]-1300, origin[1])
            
            matVector.inputs[0].default_value = 1
            matVector.inputs[1].default_value = 1
        
        # CREATE BASE COLOR
        if props.dir_color:
            mat.node_tree.nodes["StandardMaterial"].inputs[1].default_value = False # Open RS Base Dropdown
            base_color = create_node('rsTextureSamplerShaderNode', origin[0]-400, origin[1]) # Create node
            viewport_node = create_node('ShaderNodeTexImage', origin[0]-1800, origin[1])

            origin[1] -= 400  # Offsets y-axis for the next node to be placed next to it
            
            tex = load_file(bpy.path.abspath(props.dir_color)) # Load texture to file
            base_color.inputs[2].default_value = tex # Set file to node
            base_color.inputs[0].default_value = False # Expand General Dropdown
            viewport_node.image = tex
            base_color.label = "Base Color" # Label the node
            link_node(base_color.outputs[0], rsMaterial.inputs[2]) # Connect nodes
            
            if props.scalar_node:
                link_node(matVector.outputs[0], base_color.inputs[12])
            
        # CREATE AO
        if props.dir_ao:
            mat.node_tree.nodes["StandardMaterial"].inputs[1].default_value = False # Open RS Base Dropdown
            offset = -400
            
            ao = create_node('rsTextureSamplerShaderNode', origin[0]+offset, origin[1]+400) # Create node
            tex = load_file(bpy.path.abspath(props.dir_ao)) # Load texture to file
            tex.colorspace_settings.name = 'Raw'
            ao.inputs[2].default_value = tex # Set file to node
            ao.inputs[0].default_value = False # Expand General Dropdown
            ao.label = "AO" # Label the node
            
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
            mat.node_tree.nodes["StandardMaterial"].inputs[1].default_value = False # Open RS Base Dropdown
            metalness = create_node('rsTextureSamplerShaderNode', origin[0]-400, origin[1]) # Create node
            origin[1] -= 300  # Offsets y-axis for the next node to be placed next to it
            
            tex = load_file(bpy.path.abspath(props.dir_metallic)) # Load texture to file
            tex.colorspace_settings.name = 'Raw' # Change space
            metalness.inputs[2].default_value = tex # Set file to node
            metalness.inputs[0].default_value = False # Expand General Dropdown
            metalness.label = "Metalness" # Label the node
            link_node(metalness.outputs[0], rsMaterial.inputs[6]) # Connect nodes
            
            if props.scalar_node:
                link_node(matVector.outputs[0], metalness.inputs[12])
            
        # CREATE SPECULAR
        if props.dir_specular:
            mat.node_tree.nodes["StandardMaterial"].inputs[7].default_value = False # Open RS Reflection Dropdown
            specular = create_node('rsTextureSamplerShaderNode', origin[0]-400, origin[1]) # Create node
            origin[1] -= 300  # Offsets y-axis for the next node to be placed next to it
            
            tex = load_file(bpy.path.abspath(props.dir_specular)) # Load texture to file
            tex.colorspace_settings.name = 'Raw' # Change space
            specular.inputs[2].default_value = tex # Set file to node
            specular.inputs[0].default_value = False # Expand General Dropdown
            specular.label = "Specular" # Label the node
            link_node(specular.outputs[0], rsMaterial.inputs[8]) # Connect nodes
            
            if props.scalar_node:
                link_node(matVector.outputs[0], specular.inputs[12])
            
        # CREATE GLOSS
        if props.dir_gloss and not props.dir_rough: # Gloss and rough maps cannot be used at the same time. If a rough map is supplied, roughness will be used instead.
            mat.node_tree.nodes["StandardMaterial"].inputs[7].default_value = False # Open RS Reflection Dropdown
            gloss_invert = create_node('rsRSMathInvColorShaderNode', origin[0]-400, origin[1])
            gloss = create_node('rsTextureSamplerShaderNode', origin[0]-800, origin[1]) # Create node
            origin[1] -= 300  # Offsets y-axis for the next node to be placed next to it
            
            tex = load_file(bpy.path.abspath(props.dir_gloss)) # Load texture to file
            tex.colorspace_settings.name = 'Raw' # Change space
            gloss.inputs[2].default_value = tex # Set file to node
            gloss.inputs[0].default_value = False # Expand General Dropdown
            gloss.label = "Gloss" # Label the node
            link_node(gloss_invert.outputs[0], rsMaterial.inputs[10]) # Connect nodes
            link_node(gloss.outputs[0], gloss_invert.inputs[0]) # Connect nodes
            
            if props.scalar_node:
                link_node(matVector.outputs[0], gloss.inputs[12])
            
        # CREATE ROUGH
        if props.dir_rough:
            mat.node_tree.nodes["StandardMaterial"].inputs[7].default_value = False # Open RS Reflection Dropdown
            rough = create_node('rsTextureSamplerShaderNode', origin[0]-400, origin[1]) # Create node
            origin[1] -= 300  # Offsets y-axis for the next node to be placed next to it
            
            tex = load_file(bpy.path.abspath(props.dir_rough)) # Load texture to file
            tex.colorspace_settings.name = 'Raw' # Change space
            rough.inputs[2].default_value = tex # Set file to node
            rough.inputs[0].default_value = False # Expand General Dropdown
            rough.label = "Roughness" # Label the node
            link_node(rough.outputs[0], rsMaterial.inputs[10]) # Connect nodes
            
            if props.scalar_node:
                link_node(matVector.outputs[0], rough.inputs[12])
            
        # CREATE TRANSMISSION
        if props.dir_transmission:
            mat.node_tree.nodes["StandardMaterial"].inputs[15].default_value = False # Open RS Transmission Dropdown
            transmission = create_node('rsTextureSamplerShaderNode', origin[0]-400, origin[1]) # Create node
            origin[1] -= 300  # Offsets y-axis for the next node to be placed next to it
            
            tex = load_file(bpy.path.abspath(props.dir_rough)) # Load texture to file
            tex.colorspace_settings.name = 'Raw' # Change space
            transmission.inputs[2].default_value = tex # Set file to node
            transmission.inputs[0].default_value = False # Expand General Dropdown
            transmission.label = "Transmission" # Label the node
            link_node(transmission.outputs[0], rsMaterial.inputs[17]) # Connect nodes
            
            if props.scalar_node:
                link_node(matVector.outputs[0], transmission.inputs[12])
            
        # CREATE SSS
        if props.dir_sss:
            mat.node_tree.nodes["StandardMaterial"].inputs[25].default_value = False # Open RS Subsurface Dropdown
            sss = create_node('rsTextureSamplerShaderNode', origin[0]-400, origin[1]) # Create node
            origin[1] -= 300  # Offsets y-axis for the next node to be placed next to it
            
            tex = load_file(bpy.path.abspath(props.dir_sss)) # Load texture to file
            tex.colorspace_settings.name = 'Raw' # Change space
            sss.inputs[2].default_value = tex # Set file to node
            sss.inputs[0].default_value = False # Expand General Dropdown
            sss.label = "SSS" # Label the node
            link_node(sss.outputs[0], rsMaterial.inputs[27]) # Connect nodes
            
            if props.scalar_node:
                link_node(matVector.outputs[0], sss.inputs[12])
            
        # CREATE NORMAL
        if props.dir_normal:
            bpy.context.active_object.redshift.skipTangents = False
            bpy.ops.object.shade_smooth()
            mat.node_tree.nodes["StandardMaterial"].inputs[54].default_value = False # Open RS Geometry Dropdown
            rs_nbump = create_node('rsBumpMapShaderNode', origin[0]-400, origin[1])
            normal = create_node('rsTextureSamplerShaderNode', origin[0]-800, origin[1]) # Create node
            origin[1] -= 300  # Offsets y-axis for the next node to be placed next to it
            
            if props.normal_flip:
                rs_nbump.inputs[4].default_value = -1
            
            tex = load_file(bpy.path.abspath(props.dir_normal)) # Load texture to file
            tex.colorspace_settings.name = 'Raw' # Change space
            normal.inputs[2].default_value = tex # Set file to node
            normal.inputs[0].default_value = False # Expand General Dropdown
            normal.label = "Normal" # Label the node
            
            rs_nbump.inputs[2].default_value = props.normal_type
            
            link_node(rs_nbump.outputs[0], rsMaterial.inputs[57]) # Connect nodes
            link_node(normal.outputs[0], rs_nbump.inputs[3]) # Connect nodes
            
            if props.scalar_node:
                link_node(matVector.outputs[0], normal.inputs[12])
            
        # CREATE BUMP
        if props.dir_bump:
            mat.node_tree.nodes["StandardMaterial"].inputs[54].default_value = False # Open RS Geometry Dropdown
            rs_bump = create_node('rsBumpMapShaderNode', origin[0]-400, origin[1])
            bump = create_node('rsTextureSamplerShaderNode', origin[0]-800, origin[1]) # Create node
            
            tex = load_file(bpy.path.abspath(props.dir_normal)) # Load texture to file
            tex.colorspace_settings.name = 'Raw' # Change space
            bump.inputs[2].default_value = tex # Set file to node
            bump.inputs[0].default_value = False # Expand General Dropdown
            bump.label = "Bump" # Label the node
            
            if props.dir_normal:
                bump_blender = create_node('rsBumpBlenderShaderNode', origin[0], origin[1])
                
                link_node(bump.outputs[0], rs_bump.inputs[3]) # Connect nodes
                link_node(rs_bump.outputs[0], bump_blender.inputs[3]) # Bump to Layer 0
                link_node(rs_nbump.outputs[0], bump_blender.inputs[1]) # Normal to Input
                link_node(bump_blender.outputs[0], rsMaterial.inputs[57]) # BumpBlender to Standard
            else:
                link_node(rs_bump.outputs[0], rsMaterial.inputs[57]) # Connect nodes
                link_node(bump.outputs[0], rs_bump.inputs[3]) # Connect nodes
                
            if props.scalar_node:
                link_node(matVector.outputs[0], bump.inputs[12])
        
            origin[1] -= 300  # Offsets y-axis for the next node to be placed next to it
            
        # CREATE MATERIAL OUTPUT
        rsOutput = create_node('RedshiftMaterialOutputNode', origin[0]+400, 0)
            
        # CREATE ALPHA
        if props.dir_alpha:
            alpha = create_node('rsSpriteShaderNode', origin[0]+300, 0) # Create node
            
            tex = load_file(bpy.path.abspath(props.dir_alpha)) # Load texture to file
            alpha.inputs[3].default_value = tex # Set file to node
            alpha.inputs[2].default_value = False # Expand Stencil Dropdown
            alpha.label = "Alpha" # Label the node
            link_node(alpha.outputs[0], rsMaterial.inputs[52]) # Connect nodes
            rsMaterial.inputs[53].default_value = 1
            rsOutput.location[0] += 200
            alpha.inputs[5].default_value = props.alpha_type
            
            link_node(rsMaterial.outputs[0], alpha.inputs[1])
            link_node(alpha.outputs[0], rsOutput.inputs[0])
        else:
            link_node(rsMaterial.outputs[0], rsOutput.inputs[0])

        # CREATE EMISSION
        if props.dir_emission:
            mat.node_tree.nodes["StandardMaterial"].inputs[51].default_value = False # Open RS Emission Dropdown
            emission = create_node('rsTextureSamplerShaderNode', origin[0]-400, origin[1]) # Create node
            origin[1] -= 300  # Offsets y-axis for the next node to be placed next to it
            
            tex = load_file(bpy.path.abspath(props.dir_emission)) # Load texture to file
            tex.colorspace_settings.name = 'Raw' # Change space
            emission.inputs[2].default_value = tex # Set file to node
            emission.inputs[0].default_value = False # Expand General Dropdown
            emission.label = "Emission" # Label the node
            link_node(emission.outputs[0], rsMaterial.inputs[52]) # Connect nodes
            rsMaterial.inputs[53].default_value = 1.0
            
            if props.scalar_node:
                link_node(matVector.outputs[0], emission.inputs[12])
            
        rsMaterial.location[1] = origin[1]*0.25

        # CREATE DISPLACEMENT
        if props.dir_displacement:
            mat.node_tree.nodes["StandardMaterial"].inputs[54].default_value = False # Open RS Geometry Dropdown
            rs_disp = create_node('rsDisplacementShaderNode', origin[0], origin[1])
            displacement = create_node('rsTextureSamplerShaderNode', origin[0]-400, origin[1]) # Create node
            origin[1] -= 300  # Offsets y-axis for the next node to be placed next to it
            
            tex = load_file(bpy.path.abspath(props.dir_displacement)) # Load texture to file
            tex.colorspace_settings.name = 'Raw' # Change space
            displacement.inputs[2].default_value = tex # Set file to node
            displacement.inputs[0].default_value = False # Expand General Dropdown
            displacement.label = "Displacement" # Label the node
            bpy.context.active_object.rsTessDisp.GetTessellationEnabled = True
            bpy.context.active_object.rsTessDisp.GetDisplacementEnabled = True
            bpy.context.active_object.rsTessDisp.GetDisplacementScale = 1.0 # As of 3515 displacement wont show in the IPR unless its value is changed again
            rs_disp.inputs[2].default_value = 0.25
            
            if props.normal_type == "1":
                rs_disp.inputs[4].default_value = "2"
            
            link_node(rs_disp.outputs[0], rsOutput.inputs[1]) # Connect nodes
            link_node(displacement.outputs[0], rs_disp.inputs[1]) # Connect nodes
            
            if props.scalar_node:
                link_node(matVector.outputs[0], displacement.inputs[12])
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
            layout.label(text="Redshift is not enabled",icon="ERROR")
            
        else:
            props = scene.RMB

            layout.prop(props, "base_dir")
            layout.separator()

            row = layout.row()
            row.scale_y = 1.5
            row.operator("node.rmb_build")
            
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
            layout.separator(factor=0.5)
            layout.prop(props,"normal_type")
            layout.prop(props,"normal_flip")
            layout.separator(factor=0.5)
            layout.prop(props,"alpha_type")
            layout.separator(factor=1)
            layout.label(text="Naming Conventions:")
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