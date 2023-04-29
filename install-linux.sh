python3 -m pip install virtualenv
python3 -m virtualenv venv
. venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cd venv/bin
wget https://github.com/sass/dart-sass/releases/download/1.62.1/dart-sass-1.62.1-linux-x64.tar.gz
tar xf dart-sass-1.62.1-linux-x64.tar.gz
mv dart-sass/* .
rm -rf dart-sass*
cd ../..