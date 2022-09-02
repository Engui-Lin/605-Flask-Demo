# 605-Flask-Demo
Flask app that mimics bit.ly functionality

# Introductions to run locally

The following instruction works with `Python v3.8` and MacOS.

## How To Run
1. Install `virtualenv`:
```
$ pip3 install virtualenv
```

2. Open a terminal in the project root directory and run:
```
$ virtualenv env
```

3. Then run the command:
```
$ source env\Scripts\activate
```

4. Then install the dependencies:
```
$ (env) pip3 install -r requirements.txt
```

5. Finally start the web server:
```
$ (env) python3 app.py
```

This server will start on port 5000 by default. You can change this in `app.py` by changing the following line to this:

```python
if __name__ == "__main__":
    app.run(debug=True, port=<desired port>)
```