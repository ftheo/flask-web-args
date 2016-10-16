import flask
import flask_web_args.validator as validator
import flask_web_args.validate_wrapper as validate_wrapper

app = flask.Flask(__name__)


# The error handler accepts these three arguments.
# It will be called instead of the function view so return here whatever you want the user to see
def flask_error_handler(arg_name, arg_value, error_msg):
    return flask.jsonify({"error": error_msg})


# We need to declare our error handler for when parameters fail to be parsed
validate_wrapper.error_handler_func = flask_error_handler


@app.route('/pokemon_list')
@validate_wrapper.validate_args  # Just wrap the route with this decorator
def pokemon_list(
        # We can pass the default value. By passing the default value the arg_type will be auto-inferred
        limit=validator.Validator(default=10),
        # valid ca be a list or a custom function. We can also enforce the parameter to be passed or fail
        types=validator.Validator(arg_type=list, valid=["water", "fire"], required=True),
        ):
    # parsed values are accessible directly in the function
    return flask.jsonify({"limit": limit, "types": types})


@app.route('/pokemon_list/<pokemon>')
@validate_wrapper.validate_args
def pokemon_select(
        # use function for custom validation criteria. Return value or None if invalid
        # Required parameters (part of the url path) are automatically enforced
        pokemon=validator.Validator(valid_value=lambda x: PokemonModel.find(x)),
        # valid can also be a function
        info=validator.Validator(arg_type=str, valid=lambda x: x.endswith("_info"))
        ):
    return flask.jsonify({"pokemon": pokemon, "info": info})