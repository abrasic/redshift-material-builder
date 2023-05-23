# Redshift Material Builder
> Requires [Redshift Renderer](https://www.maxon.net/redshift) to use. Works as of 3.5.15

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
### **Use Vector Scale**
![image](https://github.com/abrasic/redshift-material-builder/assets/43157991/b757433e-541f-4cf5-8635-e2f0669edf4d)

 * When enabled, a Vector Maker will be connected to all your textures. This is useful to quickly modify the scale of all your textures at once.

### Normal Input
 * When using normal maps, this creates a bump map supporting the [type of normal map](https://help.maxon.net/r3d/blender/en-us/index.html#html/Bump+Map.html#BumpMap-InputMapType) you are using.

### Flip Scale
  * When enabled, it will use a normal scale of -1 instead of default 1.

### Alpha Input
  * When using alphas, this creates a sprite node supporting the [type of alpha map](https://help.maxon.net/r3d/blender/en-us/index.html#html/Sprite+Node.html#SpriteNode-OpacityCalculation) you'll be using.

### Naming Conventions
![image](https://github.com/abrasic/redshift-material-builder/assets/43157991/0a65d5d4-f88a-4feb-bd4c-247f20dca4a4)
  * These are the keywords that RMB uses to detect texture types. You can add your own here. They are **not** case-sensitive, and each keyword must be separated by spaces.

## Other Info
  * This is **not** a convert-from-cycles add-on. RMB acts as a baseplate creator for making new Redshift materials.
  * A cycles "Image Texture" node is placed on the left side of your built node tree. Without it, your diffuse texture won't appear in the viewport.
  * RMB does not delete nodes. So if you've changed your texture setup, you need to delete all your nodes and re-build.
  * As of Redshift 3.5.15, there is a bug where the dispalcement effects won't be visible in the IPR unless you tweak `Object Properties > Redshift > Displacement > Displacement Scale` for your selected object (just select the property and press enter, then reload the IPR).
