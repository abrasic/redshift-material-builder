# Redshift Material Builder for Blender
> Requires [Redshift Renderer](https://www.maxon.net/redshift) to use. Works as of RS 3.5.20 on Blender 4.0.1

> **This is a FREE product. However, you can still support the developer by [purchasing the product on Gumroad](https://box.gumroad.com/l/rmb) if you found it useful.**

RMB is a small utility script that creates basic PBR setups with only a couple clicks. Instead of wasting time by converting your cycles node trees into Redshift by hand, get a jump start by using RMB.

⚠️ **IMPORTANT:** This is NOT a one-to-one, "convert-from-Cycles" tool. RMB is a utility script that creates a PBR setup based on the textures you specifiy.

📖 Read the docs [here](https://github.com/abrasic/redshift-material-builder/wiki/).


## Supported Maps
Diffuse, AO, Metallic, Specular, Gloss, Roughness, Transmission, SSS, Normal, Bump, Emission, Alpha, Displacement

## Install
- Drag-and-drop the **redshift-material-builder.py** file in your `Blender/x.x/scripts/addons` folder or install it via Blender by going to `Edit > Preferences > Install...`

## Usage
![rmb](https://github.com/abrasic/redshift-material-builder/assets/43157991/7cda8dd2-5376-4254-b78a-02d572e02945)

If you have an object selected and an active material, you can find the script in the N-Panel of the Shader Editor.

You can either enter your maps manually based on their texture type, or you can choose the `Folder` they are in, and RMB will attempt to automatically fill the slots based on the set keywords. When you're done, simply click **Build** and RMB will do the rest.

## NEW! Build from Nodes
Alternative to Building from Files, you can also build a setup directly from the image nodes that are on the active material. Simply assign your images to their correct texture type and you're set!
![g](https://github.com/abrasic/redshift-material-builder/assets/43157991/1738606e-4bf8-43bb-aba5-cd00fc064a7d)
