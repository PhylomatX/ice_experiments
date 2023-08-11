from ice.recipe import recipe 

async def say_hello():
    return "Hello World!"

recipe.main(say_hello)