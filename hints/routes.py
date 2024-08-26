import datetime

from flask import (Blueprint, flash, redirect, render_template,
                   request, session, url_for)
from markupsafe import escape

from flags import stages  # import everything from flags.py

bp = Blueprint("ctf", __name__)

current_stage = 1
hint_index = 0


@bp.route("/flags", methods=["GET", "POST"])
@bp.route("/flags.html", methods=["GET", "POST"])
def flags():
    global current_stage, hint_index
    # initialize session variables
    if "submitted_flags" not in session:
        session["submitted_flags"] = []
    if "current_stage" not in session:
        session["current_stage"] = 1
    if "hint_index" not in session:
        session["hint_index"] = 0

    current_stage = session["current_stage"]
    submitted_flags = session["submitted_flags"]
    hint_index = session["hint_index"]


    # need to verify that the user didn't try to skip stages or trick the system

    if request.method == "POST":
        if "submit_flag" in request.form:
            submitted_flag = request.form.get("flag")
            submitted_flag = escape(submitted_flag.strip())
            # make sure its ascii only and not invalid
            if not submitted_flag.isascii():
                flash("Invalid flag. Please try again.", "danger")
                return redirect(url_for("ctf.flags"))
            
            if submitted_flag in submitted_flags:
                flash("You already submitted this flag.", "info")
            elif submitted_flag == stages[current_stage]["flag"]:
                flash(f"Correct flag for Stage {current_stage}!", "success")
                if submitted_flag not in submitted_flags:
                    submitted_flags.append(submitted_flag)
                    session["submitted_flags"] = submitted_flags
                    
                if current_stage < len(stages):
                    current_stage += 1
                    hint_index = 0
                elif current_stage == len(stages):
                    flash(
                        "You have completed all the stages. Congratulations!",
                        "success")
                    return render_template("message.html", title="Congratulations!", message="You have completed all the stages of the CTF. ")
                    # if the user has completed all the stages, then flash a
                    # message
                session["current_stage"] = current_stage
            else:
                found = False
                # if the flag is for a different stage, then put them on their
                # stage
                for stage, stage_data in stages.items():
                    if submitted_flag == stage_data["flag"]:
                        flash(
                            f"That's the flag for stage {stage}, but in the wrong order", "info", )
                        current_stage = stage
                        hint_index = 0
                        found = True
                          
                        if submitted_flag not in submitted_flags:
                            submitted_flags.append(submitted_flag)
                            session["submitted_flags"] = submitted_flags
                            
                        # check if they got all the flags (even if they are out of order)
                        if sorted(submitted_flags) == sorted([stage_data["flag"] for stage_data in stages.values()]):
                            flash(
                                "You have completed all the stages. Congratulations!",
                                "success",
                            )
                            return render_template("message.html", title="Congratulations!", message="You have completed all the stages of the CTF. ")
                            # if the user has completed all the stages, then flash a
                            # message
                        break
                # else:
                if not found:
                    flash("Incorrect flag. Try again.", "danger")

        elif "reveal_hint" in request.form:
            # hint_num = request.form.get("reveal_hint")
            if (
                hint_index < len(stages[current_stage]["hints"])
            ):  # if there are more hints to reveal
                hint_index += 1
            else:
                # if the user exhausted all the hints, have it show from the
                # beginning
                # hint_index = 0
                # flash a message to the user
                flash("Exhausted all hints for this stage :( Try harder!", "warning")
                # hide the button till they get to next stage
    session["hint_index"] = hint_index
    hints = stages[current_stage]["hints"][: hint_index]
    notes = stages[current_stage].get("notes")
    return render_template(
        "flags.html",title=f"CTFlask - Stage {current_stage}",
        stage=current_stage,
        hints=hints,
        hint_index=hint_index,
        submitted_flags=submitted_flags,
        num_hints=len(stages[current_stage]["hints"]),notes=notes
    )


@bp.route("/", methods=["GET"])  # also for index
@bp.route("/index", methods=["GET"])
@bp.route("/home", methods=["GET"])
@bp.route("/index.html", methods=["GET"])
def index():
    # initialize session variables
    if "submitted_flags" not in session:
        session["submitted_flags"] = []
    if "current_stage" not in session:
        session["current_stage"] = 1
    if "hint_index" not in session:
        session["hint_index"] = 0
        
    flash("Welcome to the CTF, please read the following:", "info")
    brief = """
    Using this site is not required to solve the CTF challenge and is not a part of the CTF challenge itself, but a tool to help you keep track of your progress. You need to find the flags on your own and not via this site itself. Good luck!
    \n
    Do not use this site for any illegal activities, please do not attack it in any way as it harms other users who are solving the CTF. The site collects logs for security purposes.
    \n
    """
    # everywhere where is /n, replace with <br> for html
    brief = brief.split("\n")

    return render_template("index.html", summary=brief, title="CTFlask - Home")


@bp.route("/restart", methods=["GET"])
@bp.route("/restart.html", methods=["GET"])
@bp.route("/reset", methods=["GET"])
@bp.route("/reset.html", methods=["GET"])
def restart():
    session.clear()
    flash("Progress reset. You are back to Stage 1.", "info")
    # reroute to index
    return redirect(url_for("ctf.index"))


# error pages
@bp.app_errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


# nice page for anything else using message.html and return 500
@bp.app_errorhandler(500)
def internal_server_error(error):
    return (
        render_template(
            "message.html",
            title="500 Internal Server Error",
            message="Please try again later",
        ),
        500,
    )


@bp.context_processor
def inject_today_date():
    """
    used for the footer to display the current year
    """
    return {"year": datetime.date.today().year}

if __name__ == "__main__":
    print("running from routes.py")
    app.run(debug=False, host="0.0.0.0", port=80)
