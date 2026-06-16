echo "BUILD START"

# Force pip to install despite the uv environment block
python3.12 -m pip install -r requirements.txt --break-system-packages

# Force create the directory
mkdir -p staticfiles

# Collect static files
python3.12 manage.py collectstatic --noinput --clear

echo "BUILD END"