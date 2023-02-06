import os
from app.main import app

# runs and triggers application from here rather than main file
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
