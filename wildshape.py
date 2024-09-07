multiline
<drac2>
returntext = ""
a = &ARGS&
name,args = get("name",""),argparse(a)
arg1 = (&ARGS& + ["help"])[:1]
isend, help = "end" in args, "help" in args or "help" in arg1
c, cbt = combat(), None
using(tf="92b005d9-e4e2-41fe-8ed8-0f0062adc668")
if c:
	cbt = tf.getCombatants(args)[0]
	if not cbt:
		return ctx.prefix + "echo Unable to locate target for wildshape " + "end" if isend else ""
else:
	return ctx.prefix + "echo This alias is designed to help with initiative, you are not in initiative"
if help:
	helptext = get_gvar("fa12f642-47f7-48b4-8289-5d1a101be028").replace("{prefix}",ctx.prefix).replace("{alias}",ctx.alias)
	returntext += f'''{ctx.prefix}embed -title "{name} Needs wildshape help" -desc "{helptext}" -footer "{ctx.prefix+ctx.alias} | by vaguely_happy" \n'''

elif isend:
	meta = tf.getMetadata(cbt)
	revertname = meta.name if "name" in meta else ""
	if revertname == character().name:
		returntext += tf.resumeChar(cbt, args) + "\n"
		returntext += ctx.prefix + "test {{using(tf='92b005d9-e4e2-41fe-8ed8-0f0062adc668')}}{{tf.transferFromWildshape(tf.getCombatantByName('"+ cbt.name +"'), combat().me,[])}}{{'Transferring back to character'}}" + "\n"
		if c.current.name == cbt.name:
			returntext += tf.moveInit(revertname) + "\n"
		returntext += tf.removeCbt(cbt, args) + "\n"
	
	else:
		returntext = ctx.prefix + "echo could not find any wildshape to end for " + cbt.name + " or you need to set your character to revert to " + revertname
	
else:
	monster = arg1[0]
	newname = tf.getMonstername(cbt, monster)
	returntext += tf.genAddMonster(cbt, monster, args) + "\n"
	returntext += ctx.prefix + "test {{using(tf='92b005d9-e4e2-41fe-8ed8-0f0062adc668')}}{{tf.transferToWildshape(tf.getCombatantByName('" + cbt.name + "'), tf.getCombatantByName('" + newname + "'),[])}}{{'Setting up the wildshape'}}" + "\n"
	if c.current.name == cbt.name:
		returntext += tf.moveInit(newname) + "\n"
	returntext += tf.removeCbt(cbt, args) + "\n"

	
return returntext

</drac2>
