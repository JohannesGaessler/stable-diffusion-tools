## Evolutionary txt2img

Starts with a list of keywords and uses them to progressively build prompts based on user feedback.

### Installation

1. Install [this script](https://github.com/hlky/stable-diffusion-webui). 
   Note that as of right now there are rapid changes every day which may break this script. Revision 3389056 is confirmed to work.
3. Download `evolutional_txt2img.py` and put it in the `scripts` directory (same directory as `webui.py`).
4. Download `map.yaml` for an example configuration file (optional but recommended).

### Usage

1. Write a YAML configuration file (or just edit the example file provided).
2. Navigate to the root directory of your Stable Diffusion installation (same directory from which to run `webui.py`).
3. Launch `evolutional_txt2img.py` and point the `--cli` argument at the configuration file. 
   **Warning: the user-provided value for `outdir` is overridden by `evolutional_txt2img.py`. Edit the config file instead.**
4. During generation YAML info files will be written at the same location as the grid images.
   These info files have a property `rating` with a default value of 0.
   Set `rating` to any numerical value to give the algorithm feedback regarding which samples you think look good or bad.
   A high value means the sample looks good, a low/negative value means you think the sample looks bad.
   All that matters with `rating` is whether values are higher or lower relative to one another.
   The absolute values do **not** matter, the algorithm only checks which of two values is higher or lower.
   If no feedback is given the algorithm will merely perform randomization without optimization.
5. Terminate the script eventually. If left to its own the script will simply run forever.
