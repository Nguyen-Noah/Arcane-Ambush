# Diff Details

Date : 2023-10-19 17:13:54

Directory c:\\Users\\nohan\\Desktop\\Projects\\Original\\Tower Defense

Total : 59 files,  775 codes, 27 comments, 73 blanks, all 875 lines

[Summary](results.md) / [Details](details.md) / [Diff Summary](diff.md) / Diff Details

## Files
| filename | language | code | comment | blank | total |
| :--- | :--- | ---: | ---: | ---: | ---: |
| [data/config/entities.json](/data/config/entities.json) | JSON | 5 | 0 | 0 | 5 |
| [data/config/hitboxes.json](/data/config/hitboxes.json) | JSON | 4 | 0 | 0 | 4 |
| [data/config/input.json](/data/config/input.json) | JSON | 40 | 0 | 0 | 40 |
| [data/config/level_data.json](/data/config/level_data.json) | JSON | -35 | 0 | 0 | -35 |
| [data/config/obst_hitboxes.json](/data/config/obst_hitboxes.json) | JSON | 1 | 0 | 0 | 1 |
| [data/config/projectiles.json](/data/config/projectiles.json) | JSON | 9 | 0 | 0 | 9 |
| [data/config/towers.json](/data/config/towers.json) | JSON | 37 | 0 | -6 | 31 |
| [data/graphics/animations/death_sparks/config.json](/data/graphics/animations/death_sparks/config.json) | JSON | 1 | 0 | 0 | 1 |
| [data/graphics/animations/knight_walk_down/config.json](/data/graphics/animations/knight_walk_down/config.json) | JSON | 1 | 0 | 0 | 1 |
| [data/graphics/animations/knight_walk_side/config.json](/data/graphics/animations/knight_walk_side/config.json) | JSON | 1 | 0 | 0 | 1 |
| [data/graphics/animations/knight_walk_up/config.json](/data/graphics/animations/knight_walk_up/config.json) | JSON | 1 | 0 | 0 | 1 |
| [data/graphics/animations/mega_slime_die_down/config.json](/data/graphics/animations/mega_slime_die_down/config.json) | JSON | 1 | 0 | 0 | 1 |
| [data/graphics/animations/mega_slime_die_side/config.json](/data/graphics/animations/mega_slime_die_side/config.json) | JSON | 1 | 0 | 0 | 1 |
| [data/graphics/animations/mega_slime_die_up/config.json](/data/graphics/animations/mega_slime_die_up/config.json) | JSON | 1 | 0 | 0 | 1 |
| [data/graphics/animations/player_die_side/config.json](/data/graphics/animations/player_die_side/config.json) | JSON | 1 | 0 | 0 | 1 |
| [data/graphics/animations/slime_die_down/config.json](/data/graphics/animations/slime_die_down/config.json) | JSON | 1 | 0 | 0 | 1 |
| [data/graphics/animations/slime_die_side/config.json](/data/graphics/animations/slime_die_side/config.json) | JSON | 1 | 0 | 0 | 1 |
| [data/graphics/animations/slime_die_up/config.json](/data/graphics/animations/slime_die_up/config.json) | JSON | 1 | 0 | 0 | 1 |
| [data/maps/Tiled Files/tutorial.tmx](/data/maps/Tiled%20Files/tutorial.tmx) | XML | 313 | 0 | 1 | 314 |
| [data/maps/tutorial/collideables.tsx](/data/maps/tutorial/collideables.tsx) | TypeScript JSX | 37 | 0 | 1 | 38 |
| [data/maps/tutorial/decorations.tsx](/data/maps/tutorial/decorations.tsx) | TypeScript JSX | 4 | 0 | 1 | 5 |
| [data/maps/tutorial/ground.tsx](/data/maps/tutorial/ground.tsx) | TypeScript JSX | 4 | 0 | 1 | 5 |
| [data/maps/tutorial/tutorial_Collideables.csv](/data/maps/tutorial/tutorial_Collideables.csv) | CSV | 23 | 0 | 1 | 24 |
| [data/maps/tutorial/tutorial_Decorations.csv](/data/maps/tutorial/tutorial_Decorations.csv) | CSV | 20 | 0 | 1 | 21 |
| [data/maps/tutorial/tutorial_Ground.csv](/data/maps/tutorial/tutorial_Ground.csv) | CSV | 19 | 0 | 1 | 20 |
| [data/maps/tutorial/tutorial_Path.csv](/data/maps/tutorial/tutorial_Path.csv) | CSV | 5 | 0 | 1 | 6 |
| [game.py](/game.py) | Python | 1 | 4 | 1 | 6 |
| [scripts/assets.py](/scripts/assets.py) | Python | 6 | 0 | -1 | 5 |
| [scripts/builder.py](/scripts/builder.py) | Python | -15 | 0 | -4 | -19 |
| [scripts/builder_menu.py](/scripts/builder_menu.py) | Python | 15 | 0 | 3 | 18 |
| [scripts/camera.py](/scripts/camera.py) | Python | 20 | 0 | 2 | 22 |
| [scripts/core_funcs.py](/scripts/core_funcs.py) | Python | 14 | 0 | 3 | 17 |
| [scripts/destruction_particles.py](/scripts/destruction_particles.py) | Python | -50 | 0 | -10 | -60 |
| [scripts/entities.py](/scripts/entities.py) | Python | 11 | 0 | 2 | 13 |
| [scripts/entity.py](/scripts/entity.py) | Python | 54 | 8 | 10 | 72 |
| [scripts/entity_map.py](/scripts/entity_map.py) | Python | 2 | 0 | 0 | 2 |
| [scripts/entity_objs/kingslime.py](/scripts/entity_objs/kingslime.py) | Python | 3 | 0 | 2 | 5 |
| [scripts/entity_objs/knight.py](/scripts/entity_objs/knight.py) | Python | 18 | 0 | 4 | 22 |
| [scripts/entity_objs/megaslime.py](/scripts/entity_objs/megaslime.py) | Python | 3 | 0 | 2 | 5 |
| [scripts/entity_objs/player.py](/scripts/entity_objs/player.py) | Python | 8 | -3 | -4 | 1 |
| [scripts/entity_objs/slime.py](/scripts/entity_objs/slime.py) | Python | -23 | 6 | -1 | -18 |
| [scripts/hitboxes.py](/scripts/hitboxes.py) | Python | -1 | 0 | 0 | -1 |
| [scripts/input.py](/scripts/input.py) | Python | 9 | 0 | 2 | 11 |
| [scripts/projectiles.py](/scripts/projectiles.py) | Python | -16 | 0 | -2 | -18 |
| [scripts/renderer.py](/scripts/renderer.py) | Python | 22 | 6 | 4 | 32 |
| [scripts/skills.py](/scripts/skills.py) | Python | -15 | -1 | -2 | -18 |
| [scripts/spawner.py](/scripts/spawner.py) | Python | -2 | 0 | 3 | 1 |
| [scripts/tower.py](/scripts/tower.py) | Python | 126 | 0 | 29 | 155 |
| [scripts/tower_map.py](/scripts/tower_map.py) | Python | 12 | 0 | 1 | 13 |
| [scripts/tower_objs/archer.py](/scripts/tower_objs/archer.py) | Python | 6 | 0 | 2 | 8 |
| [scripts/tower_objs/bomber.py](/scripts/tower_objs/bomber.py) | Python | 6 | 0 | 2 | 8 |
| [scripts/tower_objs/cleric.py](/scripts/tower_objs/cleric.py) | Python | 6 | 0 | 2 | 8 |
| [scripts/tower_objs/phoenix.py](/scripts/tower_objs/phoenix.py) | Python | 6 | 0 | 2 | 8 |
| [scripts/tower_objs/wizard_tower.py](/scripts/tower_objs/wizard_tower.py) | Python | 18 | 0 | 5 | 23 |
| [scripts/towers.py](/scripts/towers.py) | Python | 29 | 0 | 8 | 37 |
| [scripts/weapon.py](/scripts/weapon.py) | Python | -1 | 0 | 0 | -1 |
| [scripts/weapon_anim.py](/scripts/weapon_anim.py) | Python | -25 | 0 | -5 | -30 |
| [scripts/window.py](/scripts/window.py) | Python | 11 | 0 | 3 | 14 |
| [scripts/world.py](/scripts/world.py) | Python | 20 | 7 | 8 | 35 |

[Summary](results.md) / [Details](details.md) / [Diff Summary](diff.md) / Diff Details