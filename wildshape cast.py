multiline
<drac2>
returntext = ""
a = &ARGS&
name,args = get("name",""),argparse(a)
arg1 = (&ARGS& + ["help"])[:1]
isend, help = "end" in args, "help" in args or "help" in arg1
c, cbt = combat(), None
using(tf="dd6ac3c1-f5b6-46a5-950e-b4e3b0ddbb34")
if c:
	cbt = c.current
	if not cbt and not help:
		return ctx.prefix + "echo Unable to locate target for wildshape " + "end" if isend else ""
elif not help:
	return ctx.prefix + "echo This alias is designed to help with initiative, you are not in initiative"
if help:
	helptext = get_gvar("fa12f642-47f7-48b4-8289-5d1a101be028").replace("{prefix}",ctx.prefix).replace("{alias}",ctx.alias)
	returntext += f'''{ctx.prefix}embed -title "{name} Needs wildshape help" -desc "{helptext}" -footer "{ctx.prefix+ctx.alias} | by vaguely_happy" \n'''


else:
	meta = tf.getMetadata(cbt)
	revertname = meta.name if "name" in meta else ""
	
	if c.current:
		setcbt = c.current.name
	else:
		return ctx.prefix + "echo Wildshaped combatant must be current in init to perform a wildshape action"
	if revertname == character().name:
		returntext += tf.resumeChar(cbt, args) + "\n"
		returntext += ctx.prefix + "test {{using(tf='dd6ac3c1-f5b6-46a5-950e-b4e3b0ddbb34')}}{{tf.transferToWildshape(tf.getCombatantByName('"+ setcbt +"'), tf.getCombatantByName('" + revertname + "'),[])}}" + "\n"
		returntext += tf.moveInit(revertname) + "\n" # Will fail if the revert failed
		returntext += ctx.prefix + "init cast " + %*% + "\n"
		returntext += ctx.prefix + "test {{using(tf='dd6ac3c1-f5b6-46a5-950e-b4e3b0ddbb34')}}{{tf.transferToWildshape(tf.getCombatantByName('"+ revertname +"'), tf.getCombatantByName('" + setcbt + "'),[])}}" + "\n"
		returntext += tf.moveInit(setcbt) + "\n" 
		returntext += ctx.prefix + "init remove " + revertname
	
	else:
		returntext = ctx.prefix + "echo You should have your character current to cast the spell " + revertname + " : " + character().name
	


	
return returntext

</drac2>
