# Redshift Material Builder for Blender
> Requires [Redshift Renderer](https://www.maxon.net/redshift) to use. Works as of 3.5.17

> **This is a FREE product. However, you can still support the developer by [purchasing the product on Gumroad](https://box.gumroad.com/l/rmb) if you found it useful.**

RMB is a small utility script that creates basic PBR setups with only a couple clicks. Instead of wasting time by converting your cycles node trees into Redshift by hand, get a jump start by using RMB.

## Supported Maps
Diffuse, AO, Metallic, Specular, Gloss, Roughness, Transmission, SSS, Normal, Bump, Emission, Alpha, Displacement

## Install
- Drag-and-drop the **redshift-material-builder.py** file in your `Blender/3.x/scripts/addons` folder or install it via Blender by going to `Edit > Preferences > Install...`

## Usage
![rmb](https://github.com/abrasic/redshift-material-builder/assets/43157991/7cda8dd2-5376-4254-b78a-02d572e02945)

If you have an object selected and an active material, you can find the script in the N-Panel of the Shader Editor.

You can either enter your maps manually based on their texture type, or you can choose the `Folder` they are in, and RMB will attempt to automatically fill the slots based on the set keywords. When you're done, simply click **Build** and RMB will do the rest.

## Settings
### **Add Vector for Texture Scale**
![image](https://github.com/abrasic/redshift-material-builder/assets/43157991/b757433e-541f-4cf5-8635-e2f0669edf4d)

 * When enabled, a Vector Maker will be connected to all your textures. This is useful to quickly modify the scale of all your textures at once.

### **Add Image Texture Node**
![image](https://github.com/abrasic/redshift-material-builder/assets/43157991/dbaa5673-195e-407d-96b8-8289a244cace)

 * When enabled, an Image Node will be placed to the side of your node tree so you're able to see the diffuse map in your viewport solid view.

### **Add rsColorCorrect for Color**
![image](https://github.com/abrasic/redshift-material-builder/assets/43157991/f71f0e30-7c5b-4738-90e5-70f0d0123e70)

 * When enabled, a Color Correct node will be connected to your color map.

### Diffuse Color Space
 * Lets you change the color space that is used for the diffuse map. You can select between sRGB, ACEScg or Rec. 709 (utilizing Rec. 709 for Redshift [requires OCIO call before Blender startup](https://redshift.maxon.net/topic/37435/).

### Normal Input
 * When using normal maps, this creates a bump map supporting the [type of normal map](https://help.maxon.net/r3d/blender/en-us/index.html#html/Bump+Map.html#BumpMap-InputMapType) you are using.

### Alpha Input
  * When using alphas, this creates a sprite node supporting the [type of alpha map](https://help.maxon.net/r3d/blender/en-us/index.html#html/Sprite+Node.html#SpriteNode-OpacityCalculation) you'll be using.

### Diffuse is Alpha
  * Instead of an independent alpha map, the alpha channel of the diffuse map may be used instead.

### Normal/Bump/Displacement Scale
  * Sets the scale for the specified bump mapping systems.

### UV Map
  * The UV map to be used for building the material.

### Use UDIM
  * When enabled, all texture sources will use UDIM tiles.

### Delete Nodes Before Build
  * Deletes all nodes in the active material before building.

### Texture Keywords
![image](https://github.com/abrasic/redshift-material-builder/assets/43157991/0a65d5d4-f88a-4feb-bd4c-247f20dca4a4)
  * These are the keywords that RMB uses to detect texture types. You can add your own here. They are **not** case-sensitive, and each keyword must be separated by spaces.

## Other Info
  * This is **not** a convert-from-cycles add-on. RMB acts as a kickstarter for creating new Redshift materials.
  * As of Redshift 3.5.15, there is a bug where the dispalcement effects won't be visible in the IPR unless you tweak `Object Properties > Redshift > Displacement > Displacement Scale` for your selected object (just select the property and press enter, then reload the IPR).
