from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response, session
import datetime
from flags import stages
bp = Blueprint('ctf', __name__)



current_stage = 1
hint_index = 0

@bp.route('/flags', methods=['GET', 'POST'])
@bp.route('/flags.html', methods=['GET', 'POST'])
def flags():
    global current_stage, hint_index
    # initialize session variables
    if "submitted_flags" not in session:
        session['submitted_flags'] = []
    if "current_stage" not in session:
        session['current_stage'] = 1
    
    current_stage = session['current_stage']
    submitted_flags = session['submitted_flags']
    # need to verify that the user didn't try to skip stages or trick the system
    
    if request.method == 'POST':
        if 'submit_flag' in request.form:
            submitted_flag = request.form.get('flag')
            if submitted_flag == stages[current_stage]['flag']:
                flash(f"Correct flag for Stage {current_stage}!", 'success')
                submitted_flags.append(submitted_flag)
                session['submitted_flags'] = submitted_flags
                if current_stage < len(stages):
                    current_stage += 1
                    hint_index = 0
                elif current_stage == len(stages):
                    flash("You have completed all the stages. Congratulations!", 'success')
                    # if the user has completed all the stages, then flash a message
                session['current_stage'] = current_stage
            else:
                found = False
                # if the flag is for a different stage, then put them on their stage
                for stage, stage_data in stages.items():
                    if submitted_flag == stage_data['flag']:
                        flash(f"That's the flag for stage {stage}, but in the wrong order", 'info')
                        current_stage = stage
                        hint_index = 0
                        found = True
                        break
                # else:
                if not found:
                    flash("Incorrect flag. Try again.", 'danger')
        
        elif 'reveal_hint' in request.form:
            if hint_index < len(stages[current_stage]['hints']) - 1: # if there are more hints to reveal
                hint_index += 1
            else:
                # if the user exhausted all the hints, have it show from the beginning
                hint_index = 0
                # flash a message to the user
                
                flash("No new hints :( Try harder!", 'info')
                
    hints = stages[current_stage]['hints'][:hint_index + 1]
    return render_template('flags.html', stage=current_stage, hints=hints, hint_index=hint_index, submitted_flags=submitted_flags)


@bp.route('/', methods=['GET']) # also for index
@bp.route('/index', methods=['GET'])
@bp.route('/home', methods=['GET'])
@bp.route('/index.html', methods=['GET'])
def index():
     # initialize session variables
    if "submitted_flags" not in session:
        session['submitted_flags'] = []
    if "current_stage" not in session:
        session['current_stage'] = 1
        
    flash("Welcome to the CTF, please read the following messages: ", 'info')
    brief = """
    This site is not required to solve the CTF challenge. It does not store any of your flags, so make sure to keep track of them yourself! 
    \n
    Do not use this site for any illegal activities, please do not attack it in any way as it harms other users who are solving the CTF.
    The site collects logs for security purposes. 
    This site is not a part of the CTF challenge itself, but a tool to help you keep track of your progress. The flags are not hidden on this site. You need to find them on your own. Good luck!
    \n
    """
    
    return render_template('index.html', summary=brief)

@bp.route('/restart', methods=['GET'])
@bp.route('/restart.html', methods=['GET'])
@bp.route('/reset', methods=['GET'])
@bp.route('/reset.html', methods=['GET'])
def restart():
    session.clear()
    flash("Progress reset. You are back to Stage 1.", 'info')
    # reroute to index
    return redirect(url_for('ctf.index'))
    # resp = make_response(redirect(url_for('ctf.index')))
    # resp.set_cookie('stage', '1', httponly=True)
    # resp.set_cookie('hint_index', '0', httponly=True)
    # flash("Progress reset. You are back to Stage 1.", 'info')
    # return resp



@bp.context_processor
def inject_today_date():
    """
    used for the footer to display the current year
    """
    return {'year': datetime.date.today().year}