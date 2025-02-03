# Created by `pipx` on 2025-01-30 09:55:02
export PATH="$PATH:/Users/magdolinharmina/.local/bin"

# Poetry path
export PATH="/Users/magdolinharmina/.local/bin:$PATH"

# Python path (if needed)
export PATH="/Users/magdolinharmina/Library/Caches/pypoetry/virtualenvs/trip-planner-from-scratch-BbbxfJrc-py3.13/bin:$PATH"

# Add Poetry completion if you want it
fpath+=~/.zfunc
autoload -Uz compinit && compinit

# Optional: Add alias for poetry commands if you want shortcuts
alias po="poetry"
alias posh="poetry shell"
alias poru="poetry run"

poetry env use python3.13
poetry install
poetry shell
