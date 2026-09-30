# Visual Asset Manifest — Packaging Repair

Selected proof asset: Quaternius Modular SciFi MegaKit `Column_Astra.gltf`.
Source: https://quaternius.com/packs/modularsci-fi.html. License: CC0.

| File | Original size | Destination / imported size | Role |
| --- | ---: | ---: | --- |
| `glTF/Columns/Column_Astra.gltf` | 5,688 B | `public/world/assets/v2/quaternius/Column_Astra.gltf` / 5,688 B | visible Central Plaza column |
| `glTF/Columns/Column_Astra.bin` | 5,404 B | `public/world/assets/v2/quaternius/Column_Astra.bin` / 5,404 B | geometry buffer |
| `Textures/T_Trim_03_Normal.png` | 375,307 B | same directory / 375,307 B | image URI dependency |
| `Textures/T_Trim_03_BaseColor.png` | 1,285,125 B | same directory / 1,285,125 B | image URI dependency |
| `Textures/T_Trim_03_ORM.png` | 3,009,230 B | same directory / 3,009,230 B | image URI dependency |
| `Textures/T_Trim_02_Normal.png` | 756,841 B | same directory / 756,841 B | image URI dependency |
| `Textures/T_Trim_02_BaseColor_Red.png` | 1,150,649 B | same directory / 1,150,649 B | image URI dependency |
| `Textures/T_Trim_02_ORM.png` | 3,994,352 B | same directory / 3,994,352 B | image URI dependency |
| `Textures/T_Trim_01_Normal.png` | 585,626 B | same directory / 585,626 B | image URI dependency |
| `Textures/T_Trim_01_BaseColor_Red.png` | 965,873 B | same directory / 965,873 B | image URI dependency |
| `Textures/T_Trim_01_ORM.png` | 3,338,790 B | same directory / 3,338,790 B | image URI dependency |

All nine image URIs and the single buffer URI are resolved by the deterministic
world asset dependency guard. No remote, data, or path-escaping URI is allowed.
