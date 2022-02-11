from flask import jsonify
from flask import request, session, redirect
from flask import Blueprint
from application.okta.helpers import  is_authorized

okta_routes = Blueprint("okta_routes", __name__)

@okta_routes.route('/authenticate', methods=["GET", "POST"])
def authenticate():
    if not is_authorized(request):
        return "Unauthorized", 401

    return jsonify({"message": True})
        