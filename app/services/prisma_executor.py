import textwrap
import asyncio
from app.prisma import Prisma

async def execute_prisma_code(code: str, db: Prisma):
    """
    Safely executes dynamically generated Prisma Python async code.
    Assumes `code` contains a valid python snippet that assigns the final output to a variable named `result`.
    """
    # Clean up markdown if any
    code = code.strip()
    if code.startswith("```python"):
        code = code.split("```python")[1].split("```")[0].strip()
    elif code.startswith("```"):
        code = code.split("```")[1].split("```")[0].strip()

    # Wrap the user code in an async function so we can await it
    wrapped_code = f"""
async def __dynamic_execution(db):
    import json
{textwrap.indent(code, '    ')}
    return result
"""
    local_env = {}
    def compile_code():
        exec(wrapped_code, {}, local_env)
        
    try:
        # Offload compilation (synchronous blocking) to OS thread pool
        await asyncio.to_thread(compile_code)
        
        func = local_env['__dynamic_execution']
        res = await func(db)
        
        # Ensure the result is formatted as a string to pass back to formatting agent
        if hasattr(res, 'model_dump_json'):
            return res.model_dump_json()
        elif isinstance(res, list):
            total_records = len(res)
            # Truncate to max 50 records to prevent LLM context overflows
            sliced_res = res[:50]
            if len(sliced_res) > 0 and hasattr(sliced_res[0], 'model_dump_json'):
                import json
                truncated_data = json.dumps([json.loads(r.model_dump_json()) for r in sliced_res])
                if total_records > 50:
                    return f"{{'note': 'Result truncated. Showing 50 of {total_records} records.', 'data': {truncated_data}}}"
                return truncated_data
            
            if total_records > 50:
                return f"{{'note': 'Result truncated. Showing 50 of {total_records} records.', 'data': {str(sliced_res)}}}"
            
        return str(res)
    except Exception as e:
        return f"Execution Error: {str(e)}\nCode attempted: {code}"
