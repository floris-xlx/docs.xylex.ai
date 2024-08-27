if [ -f "./requirements.txt" ]; then
    pip install -r ./requirements.txt
    echo "docs.xylex.ai: requirements.txt installed."
else
    echo "docs.xylex.ai: requirements.txt not found."
fi
