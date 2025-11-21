# Install python 3.13 and make it the default
brew update
brew install pyenv
pyenv install 3.13
pyenv global 3.13

# Add this to your ~/.zshrc
export PYENV_ROOT="$HOME/.pyenv"
eval "$(pyenv init -)"

# Save required python packages:
pip freeze > requirements.txt

# install required packages
pip install -r requirements.txt

