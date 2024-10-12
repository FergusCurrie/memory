from contextlib import redirect_stderr, redirect_stdout
import logging 


logger = logging.getLogger(__name__)

import io 



def _gen_code(code, local_variables={}):
    output = io.StringIO()
    error = io.StringIO()
    try:
        with redirect_stdout(output), redirect_stderr(error):
            exec(code, {}, local_variables)
        logger.info("raise exception")
        return local_variables, None
    except Exception as e:
        logger.info(f"Exception hit {e} {error}")
        error_output = error.getvalue().strip()
        if error_output:
            logger.info(error_output)
            return {}, error_output
        return {}
    
def multi_choice_generation(problem):
    assert 'generation_code' in problem 


    # 1. Generate the problem 

    local_variables, error = _gen_code(problem['generation_code'])

    # 2. Update description to contain generated problem 
    description = problem['description']
    for key, value in local_variables.items():
        if 'input' in key or 'option' in key:
            description = description.replace('{' + f"{key}" +'}', f"{value}")
    # description = _add_generated_variables_to_description(local_variables, problem['description'])
    

    # Generate answer options 
    options = [str(value) for key,value in local_variables.items() if 'option' in key]

    return {
        "description": description,
        "options" : options,
        "correctAnswer": str(local_variables['correct_answer'])
    }

