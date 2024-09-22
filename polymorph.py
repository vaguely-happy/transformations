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
		return ctx.prefix + "echo Unable to locate target for polymorph " + "end" if isend else ""
	
else:
	return ctx.prefix + "echo This alias is designed to help with initiative, you are not in initiative"
if help:
	helptext = get_gvar("f586db3b-4b89-4f27-a4ad-2b54faaec393").replace("{prefix}",ctx.prefix).replace("{alias}",ctx.alias)
	returntext += f'''{ctx.prefix}embed -title "{name} Needs polymorph help" -desc "{helptext}" -footer "{ctx.prefix+ctx.alias} | by vaguely_happy" \n'''

elif isend:
	meta = tf.getMetadata(cbt)
	revertname = meta.name if "name" in meta else ""
	if c.current:
		if c.current.name == cbt.name:
			setcbt = revertname
		else:
			setcbt = c.current.name
	else:
		returntext += ctx.prefix + "init madd commoner -p 100 -name 'Pre-combat transformation' -hp -5" + "\n"
		setcbt = "Pre-combat transformation"
	if setcbt != cbt.name:
		returntext += tf.moveInit(cbt.name) + "\n"   # this will protect the current from a false deletion
	if revertname:
		returntext += tf.resume(cbt, args) + "\n"
		returntext += ctx.prefix + "tembed -title '{{name}} Is polymorphing' "
		returntext += " -desc  {{using(tf='92b005d9-e4e2-41fe-8ed8-0f0062adc668')}}{{tf.messageText(tf.getCombatantByName('" + cbt.name + "'), tf.getCombatantByName('" + revertname + "'),[])}} "
		returntext += " -f {{using(tf='92b005d9-e4e2-41fe-8ed8-0f0062adc668')}}{{tf.transferFromPoly(tf.getCombatantByName('"+ cbt.name +"'), combat().me,[])}} "
		returntext += " -footer 'polymorph - by vaguely_happy'" + "\n"
		returntext += tf.moveInit(revertname) + "\n" # Will fail if the revert failed
		returntext += tf.removeCbt(cbt, args) + "\n"  # Hence will also fail if the previous init move did not work
		if setcbt != revertname:
			returntext += tf.moveInit(setcbt) + "\n" # Put the init back where we want it
	
	else:
		returntext = ctx.prefix + "echo could not find any polymorph to end for " + cbt.name
	
else:
	monster = arg1[0]
	newname = tf.getMonstername(cbt, monster)
	if c.current:
		if c.current.name == cbt.name:
			setcbt = newname
		else:
			setcbt = c.current.name
	else:
		returntext += ctx.prefix + "init madd commoner -p 100 -name 'Pre-combat transformation' -hp -5" + "\n"
		setcbt = "Pre-combat transformation"
	if setcbt != cbt.name:
		returntext += tf.moveInit(cbt.name) + "\n"   # this will protect the current from a false deletion
	returntext += tf.genAddMonster(cbt, monster, args) + "\n"
	returntext += ctx.prefix + "tembed -title '{{name}} Is polymorphing' "
	returntext += " -desc  {{using(tf='92b005d9-e4e2-41fe-8ed8-0f0062adc668')}}{{tf.messageText(tf.getCombatantByName('" + cbt.name + "'), tf.getCombatantByName('" + newname + "'),[])}} "
	returntext += " -f {{using(tf='92b005d9-e4e2-41fe-8ed8-0f0062adc668')}}{{tf.transferToPoly(tf.getCombatantByName('"+ cbt.name +"'), tf.getCombatantByName('" + newname + "'),[])}}"
	returntext += " -footer 'polymorph - by vaguely_happy'" + "\n"
	returntext += tf.moveInit(newname) + "\n" # Will fail if the new combatant failed to add for any reason 
	returntext += tf.removeCbt(cbt, args) + "\n"  # Hence will also fail if the previous init move did not work
	if setcbt != newname:
		returntext += tf.moveInit(setcbt) + "\n" # Put the init back where we want it

return returntext

</drac2>
