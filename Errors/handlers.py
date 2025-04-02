from flask import Blueprint, render_template

errors = Blueprint("errors", __name__)

@errors.app_errorhandler(404)
def error_404(error):
  return render_template("Errors/404.html"), 404

@errors.app_errorhandler(400)
def error_400(error):
  return render_template("Errors/400.html"), 400

@errors.app_errorhandler(403)
def error_403(error):
  return render_template("Errors/403.html"), 403

@errors.app_errorhandler(405)
def error_405(error):
  return render_template("Errors/405.html"), 405

@errors.app_errorhandler(500)
def error_500(error):
  return render_template("Errors/500.html"), 500
