# Flask Web Args

A simple library to parse and validate web args in Flask. This library will validate:

1. url variables (`/user/<user_name>`)
2. url parameters (`/user?limit=5`)

What's cool about `flask-web-args` is that parsed parameters are accessed inside the function as if they were passed.

Other cool stuff you can do:

* Add default value
* Expect a list of possible values
* Define your custom function to return the parsed/valid value

## Installation

```
pip install flask_web_args
```

## Usage

```python
import flask
import flask_web_args

app = flask.Flask(__name__)


# The error handler accepts these three arguments.
# It will be called instead of the function view so return here whatever you want the user to see
def flask_error_handler(arg_name, arg_value, error_msg):
    return flask.jsonify({"error": error_msg})


# We need to declare our error handler for when parameters fail to be parsed
flask_web_args.error_handler_func = flask_error_handler


@app.route('/pokemon_list')
@flask_web_args.validate_args  # Just wrap the route with this decorator
def pokemon_list(
        # We can pass the default value. By passing the default value the arg_type will be auto-inferred
        limit=flask_web_args.Validator(default=10),
        # valid ca be a list or a custom function. We can also enforce the parameter to be passed or fail
        types=flask_web_args.Validator(arg_type=list, valid=["water", "fire"], required=True),
        ):
    # parsed values are accessible directly in the function
    return flask.jsonify({"limit": limit, "types": types})


@app.route('/pokemon_list/<pokemon>')
@flask_web_args.validate_args
def pokemon_select(
        # use function for custom validation criteria. Return value or None if invalid
        # Required parameters (part of the url path) are automatically enforced
        pokemon=flask_web_args.Validator(valid_value=lambda x: PokemonModel.find(x)),
        # valid can also be a function
        info=flask_web_args.Validator(arg_type=str, valid=lambda x: x.endswith("_info"))
        ):
    return flask.jsonify({"pokemon": pokemon, "info": info})
```

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D
