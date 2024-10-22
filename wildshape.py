multiline
<drac2>
returntext = ""
a = &ARGS&
name,args = get("name",""),argparse(a)
arg1 = (&ARGS& + ["help"])[:1]
cc = "Wild Shape"
isend, help = "end" in args, "help" in args or "help" in arg1
c, cbt, ch = combat(), None, character()

ignore = "i" in args
if not ignore and not isend:
	if not ch.cc_exists(cc):
		return ctx.prefix + "echo Unable to find counter for " + cc
	elif ch.cc(cc).value < 1:
		return ctx.prefix + "echo No uses of " + cc + " remaining : " + ch.cc_str(cc)
	

using(tf="dd6ac3c1-f5b6-46a5-950e-b4e3b0ddbb34")
if c:
	cbt = tf.getCombatants(args)[0]
	if not cbt and not help:
		return ctx.prefix + "echo Unable to locate target for wildshape " + "end" if isend else ""
elif not help:
	return ctx.prefix + "echo This alias is designed to help with initiative, you are not in initiative"
if help:
	helptext = get_gvar("fa12f642-47f7-48b4-8289-5d1a101be028").replace("{prefix}",ctx.prefix).replace("{alias}",ctx.alias)
	returntext += f'''{ctx.prefix}embed -title "{name} Needs wildshape help" -desc "{helptext}" -footer "{ctx.prefix+ctx.alias} | by vaguely_happy" \n'''


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
	if revertname == character().name:
		returntext += tf.resumeChar(cbt, args) + "\n"
		returntext += ctx.prefix + "tembed -title '{{name}} Is wildshaping' "
		returntext += " -desc  {{using(tf='dd6ac3c1-f5b6-46a5-950e-b4e3b0ddbb34')}}{{tf.messageText(tf.getCombatantByName('" + cbt.name + "'), tf.getCombatantByName('" + revertname + "'),[])}} "
		returntext += " -f {{using(tf='dd6ac3c1-f5b6-46a5-950e-b4e3b0ddbb34')}}{{tf.transferFromWildshape(tf.getCombatantByName('"+ cbt.name +"'), combat().me,[])}} "
		returntext += " -footer 'wildshape - by vaguely_happy'" + "\n"
		returntext += tf.moveInit(revertname) + "\n" # Will fail if the revert failed
		returntext += tf.removeCbt(cbt, args) + "\n"  # Hence will also fail if the previous init move did not work
		if setcbt != revertname:
			returntext += tf.moveInit(setcbt) + "\n" # Put the init back where we want it
	
	else:
		returntext = ctx.prefix + "echo could not find any wildshape to end for " + cbt.name + " or you need to set your character to revert to " + revertname
	
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
	ch.mod_cc(cc, -1)
	returntext += tf.genAddMonster(cbt, monster, args) + "\n"
	returntext += ctx.prefix + "tembed -title '{{name}} Is wildshaping' "
	returntext += " -desc  {{using(tf='dd6ac3c1-f5b6-46a5-950e-b4e3b0ddbb34')}}{{tf.messageText(tf.getCombatantByName('" + cbt.name + "'), tf.getCombatantByName('" + newname + "'),[])}} "
	returntext += " -f {{using(tf='dd6ac3c1-f5b6-46a5-950e-b4e3b0ddbb34')}}{{tf.transferToWildshape(tf.getCombatantByName('"+ cbt.name +"'), tf.getCombatantByName('" + newname + "'),[])}}"
	returntext += f''' -f "{cc} : {ch.cc_str(cc)}" '''
	returntext += " -footer 'wildshape - by vaguely_happy'" + "\n"

	returntext += tf.moveInit(newname) + "\n" # Will fail if the new combatant failed to add for any reason 
	returntext += tf.removeCbt(cbt, args) + "\n"  # Hence will also fail if the previous init move did not work
	if setcbt != newname:
		returntext += tf.moveInit(setcbt) + "\n" # Put the init back where we want it


	
return returntext

</drac2>
