echo "START"
echo "(1/2) Activating ENV 'botenv'."
source ./botenv/bin/activate
echo "(2/2) Installing requirements."
pip install -r requirements.txt
echo "END"