# Prompt-to-action pipeline for our reBot B601-DM

You type what you want, for example *"put the red block on the blue block"*. An AI (Claude) looks at the camera picture, decides what to do, and the robot arm does it.

It is built on [WRC](https://github.com/TheMoonAstronaut/wrc), an open-source robot pipeline made for the RS version of our arm. This folder adapts it to our **DM** arm.

## How it works

1. **You type a task** in a web page.
2. **The camera** takes a picture of the table.
3. **An object detector** finds the things on the table and where they are.
4. **Claude** gets the picture and the list of objects, and picks an action, such as "pick up the red block and place it on the blue block".
5. **WRC plans the motion**: where to grab the object and how each joint has to move.
6. **A safety check** looks at every small step of the motion. The arm must stay inside its allowed area, above the table, and under a speed limit. If a step fails the check, the arm stops.
7. **The arm moves**: it reaches down, closes the gripper, carries the object and lets go.
8. **Claude reports** what happened, including when something failed.

```
you type a task → Claude (sees the camera) → WRC (plans + safety check) → arm
                                                                          ├─ simulator of our DM arm   ← works today
                                                                          └─ the real DM arm           ← not tested yet
```

## What works today

- **In a physics simulation of our DM arm: yes.** Claude stacked blocks, moved objects and described the scene. Objects ended up 5 to 15 mm from where they should be. When an object was out of reach, it said so and parked the arm.
- **On the real arm: not tested.** The connection uses the same driver calls as our `teleoperation/go_ready.py`, but nobody has run this pipeline on the hardware. Start slowly and follow the checklist (link below).
- **Camera calibration: tool included, tested in the simulator only.** You print one sheet, measure two points with a ruler, and run one command.

## Try it in the simulator

You need conda, `uv`, and this repo's `teleoperation` folder set up (`./scripts/setup_assets.sh && uv sync`).

```bash
bash wrc_dm_pipeline/setup_wrc.sh          # downloads WRC next to this repo and adds our files
cd ../wrc
PYTHONNOUSERSITE=1 conda env create -f environment.yml
bash local_dm/install.sh                   # checks everything and says what is missing
echo 'ANTHROPIC_API_KEY=your-key' > .env   # your own Claude API key (never commit it)
./START_WRC.sh dm                          # opens the 3D simulator and the web page
```

Then open http://127.0.0.1:8090/ and type a task. Things to try:

- `Take the red block and stack it on top of the blue one.`
- `What objects can you see on the table right now?`
- `Move the red block to the free spot`

Without an API key it still runs, but only fixed commands work, like `pick and place the red block` or `go home`.

## Good to know

- The arm can only grab objects up to about **40 cm** in front of its base (34 cm for tall objects).
- The detector only finds objects whose **names it was given** (`--classes "red block,blue block,..."`). Change the names for your objects.
- Each task costs about 4 US cents in Claude API calls and takes 3 Claude steps of about 2 seconds each.

## What is in this folder

| Path | What it is |
|---|---|
| `setup_wrc.sh` | Downloads WRC and copies our files into it |
| `overlay/local_dm/` | Our code: the link between WRC and the DM arm (simulated or real), the Claude connection, camera calibration |
| `overlay/START_WRC.sh` | One script to start everything |
| `overlay/configs/` | Settings for the DM arm and the simulator camera |
| `overlay/local_mock/` | Earlier experiments without physics (not needed for the DM arm) |

## More detail

- **Full guide, test results, real-arm checklist, camera calibration:** [`overlay/local_dm/README.md`](overlay/local_dm/README.md)
- **How the WRC environment was set up (including the macOS fix):** [`overlay/SETUP_REPORT.md`](overlay/SETUP_REPORT.md)
