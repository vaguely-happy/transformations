# transformlib
# Methods to use in transformations - such as polymorph and wildshape
#
# This is designed to return lines which are then output in a multiline alias
# Lower level methods will produce parts of that information
#

def getCombatants(args):
	#Basic Variables
	c, combatants = combat(), []
	
	if "t" in args:
		# Target is defined so use that
		

		#Creates a list of targets that have been grabbed by -t
		targets = args.get('t')

		#This is an if statement for targets that checks if an element in it is a combatant, and appends them to the combatants list, else it gets the list of combatants from the group and joins it to the combatants list, allowing for everything to be in one list for further parsing.
		for x in targets:
		  if (combatant := combat().get_combatant(x) ):
		    combatants.append(combatant)

	else:
		# No target so self target
		combatant = c.me
		if combatant:
			combatants.append(combatant)
		else:  # This could be a wildshape so check against metadata
			meta = getMetadata(c.current)
			if "name" in meta:
				combatant = c.current
				combatants.append(combatant)
			elif c.current.type == "group":
				for gr_cbt in c.current.combatants:
					meta = getMetadata(gr_cbt)
					if "name" in meta:
						combatant = gr_cbt
						combatants.append(combatant)
		combatants.append(combatant)
	return combatants
	
def getGroup(cbt):
	c = combat()
	for group in c.groups:
		for grp_cbt in group.combatants:
			if grp_cbt.name == cbt.name:
				return group
	return None
	
def getCombatantByName(name):
	c = combat()
	if (combatant := combat().get_combatant(name, strict=True) ):
		return combatant
	else:
		return None
	

def genAddMonsters(monster, args):
	commandstring = ""
	combatatants = getCombatants(args)
	for combatant in combatants:
		commandstring += genAddMonster(cbt, monster, args)
		
	
def genAddMonster(cbt, monster, args):
	commandstring = ""
	newname = getMonstername(cbt,monster)
	setMetadata(cbt, newname)
	group = getGroup(cbt)
	commandstring += f'''{ctx.prefix}init madd "{monster}" -p {cbt.init} -name "{newname}" -h'''
	commandstring += f''' -note "{cbt.note}"''' if cbt.note else ""
	commandstring += f''' -group "{group.name}"''' if group else ""
	return commandstring
	
def transferToWildshape(cbt1, cbt2, args):
	if cbt1 and cbt2:
		applyWildshape(cbt2, args)
		transferPreserveAbi(cbt1, cbt2)
		return "'Wildshape|Transferring effects to wildshape'"
	else:
		return "Wildshape|Aborted"
	
def transferToPoly(cbt1, cbt2, args):
	if cbt1 and cbt2:
		applyPoly(cbt1, cbt2, args)
		transferEffects(cbt1, cbt2)
		return "'Polymorph|Transferring effects to polymorph'"
	else:
		return "Polymorph|Aborted"
	
	
def applyPoly(cbt1, cbt2, args):
	fromthp = cbt1.temp_hp if cbt1.temp_hp else 0
	beasthp = cbt2.hp
	cbt2.set_hp(cbt1.hp)
	cbt2.set_maxhp(cbt1.max_hp)
	if beasthp > fromthp:
		cbt2.set_temp_hp(beasthp)
	else:
		cbt2.set_temp_hp(fromthp)
		
		
def applyWildshape(cbt,args):
	ch = character()
	druidlevel = ch.levels.get("Druid")
	subclassinfo = load_json(ch.get_cvar("subclass","{}"))
	subclass = subclassinfo.get("DruidLevel","")	
	wildthp = druidlevel
	if subclass and "moon" in subclass.lower():
		moonac = 13 + character().stats.get_mod("wisdom")
		if moonac > cbt.ac:
			cbt.set_ac(moonac)
		wildthp = 3 * int(druidlevel)
	druidhp = character().hp
	druidmaxhp = character().max_hp
	druidthp = character().temp_hp if character().temp_hp else 0
	cbt.set_hp(druidhp)
	cbt.set_maxhp(druidmaxhp)
	if wildthp > druidthp:
		cbt.set_temp_hp(wildthp)
	else:
		cbt.set_temp_hp(druidthp)

# Different transfers used to handle the fact that we adjust attacks for wildshape to allow for using un-adjusted monster blocks that have the wrong caster ability scores
def transferFromWildshape(cbt1, cbt2, args):
	if cbt1 and cbt2:
		endTransform(cbt1, cbt2)
		transferPreserveAbi(cbt1, cbt2)
		return "'Wildshape|Transferring effects back'"
	else:
		return "Wildshape|Aborted"
	
def transferFromPoly(cbt1, cbt2, args):
	if cbt1 and cbt2:
		endTransform(cbt1, cbt2)
		transferEffects(cbt1, cbt2)
		return "'Polymorph|Transferring effects back'"
	else:
		return "Polymorph|Aborted"
		
def transferAcross(cbt1, cbt2):
	if cbt1 and cbt2:
		endTransform(cbt1, cbt2)
		transferEffects(cbt1, cbt2)
	else:
		return "Transfer aborted, could not find combatants"

# Generic end transform seems to be how they work but I have not looked at every spell yet. Might need more specific ones later
def endTransform(cbt1, cbt2):
	cbt2.set_hp(cbt1.hp)
	cbt2.set_maxhp(cbt1.max_hp)
	if cbt1.temp_hp:
		targettmp = cbt2.temp_hp if cbt2.temp_hp else 0
		if cbt1.temp_hp > cbt2.temp_hp:
			cbt2.set_temp_hp(cbt1.temp_hp)
	
	
def setCurrCharacter(cbt,args):
	commandstring = ""
	meta = getMetadata(cbt)
	if meta and meta.owner == ctx.author.id:
		commandstring += ctx.prefix + "char " + meta.name
		
def getMonstername(cbt, monster):
	name = cbt.name
	meta = getMetadata(cbt)
	if meta and "name" in meta: # We are transforming a transform so don't chain the names or else who knows what lunacy will happen
		return f'''{meta.name}'''
	return f'''{monster} ({name})'''
	
def removeCbt(cbt, args):
	return ctx.prefix + "init remove " + cbt.name
	
	
def resume(cbt, args):
	meta = getMetadata(cbt)
	if meta and meta.monster:
		if meta.monster == "character":
			return resumeChar(cbt, args)
		else:
			return genAddMonster(cbt, meta.monster, args)
	else:
		return ctx.prefix + "echo Unable to find a transformation to end, please check that your character is currently active"
	
def resumeChar(cbt, args):
	commandstring = ""
	meta = getMetadata(cbt)
	group = getGroup(cbt)
	if meta and meta.owner == ctx.author.id:
		commandstring += f'''{ctx.prefix}init join -p {cbt.init} -name "{meta.name}"'''
		commandstring += f''' -note "{cbt.note}"''' if cbt.note else ""
		commandstring += f''' -group "{group.name}"''' if group else ""
		return commandstring
	else:
		commandstring = ctx.prefix + "echo only the controlling player of the character can end the transformation to add the character back into combat"
		return commandstring
		
# This code from Croebh in Collections/Initiative%20Utilities/effectcopy.alias	
def str_resist(resist):
	out = []
	for only in resist.get('only', []):
		out.append(only)
	for unless in resist.get('unless', []):
		out.append(f"non{unless}")
	out.append(resist['dtype'])
	return " ".join(out)
	
def passiveEffects(effect):
	passives = effect.effect.copy()
	for r_type in ('resistances', 'immunities', 'vulnerabilities', 'ignored_resistances'):
		if passives.get(r_type):
			passives[r_type] = [str_resist(i) for i in passives[r_type]]
	return passives
	
	
def transferEffects(cbt1, cbt2):
	for effect in cbt1.effects:
		children = effect.children
		try:
			neweffect = cbt2.add_effect(name = effect.name, duration = effect.remaining, concentration = effect.conc, parent = effect.parent, desc=effect.desc, passive_effects = passiveEffects(effect), buttons=effect.buttons, attacks=effect.attacks)
		except:
			neweffect = cbt2.add_effect(name = effect.name, duration = effect.remaining, concentration = effect.conc, parent = effect.parent, desc=effect.desc, passive_effects = passiveEffects(effect), attacks=effect.attacks)
		for child in children:
			ch_cbt = getCombatantByName(child.combatant_name)
			ch_cbt.remove_effect(child.name, strict = True)
			ch_effect = ch_cbt.add_effect(name = child.name, duration = child.remaining, concentration = child.conc, parent = neweffect, desc=child.desc, passive_effects = passiveEffects(child), buttons=child.buttons, attacks=child.attacks)

# Adjusts the ability scores on attacks to reflect that wildshape should preserve the mental ability scores and proficiency bonus.
def transferPreserveAbi(cbt1, cbt2):
	for effect in cbt1.effects:
		children = effect.children
		try:
			neweffect = cbt2.add_effect(name = effect.name, duration = effect.remaining, concentration = effect.conc, parent = effect.parent, desc=effect.desc, passive_effects = passiveEffects(effect), buttons=effect.buttons, attacks=adjustAttack(effect.attacks))
		except:
			neweffect = cbt2.add_effect(name = effect.name, duration = effect.remaining, concentration = effect.conc, parent = effect.parent, desc=effect.desc, passive_effects = passiveEffects(effect), attacks=adjustAttack(effect.attacks))
		for child in children:
			ch_cbt = getCombatantByName(child.combatant_name)
			ch_cbt.remove_effect(child.name, strict = True)
			ch_effect = ch_cbt.add_effect(name = child.name, duration = child.remaining, concentration = child.conc, parent = neweffect, desc=child.desc, passive_effects = passiveEffects(child), buttons=child.buttons, attacks=child.attacks)

def adjustAttack(attack):
	subs = {
	"intelligenceMod" : character().stats.get_mod("int"),
	"wisdomMod" : character().stats.get_mod("wis"),
	"charismaMod" : character().stats.get_mod("cha"),
	"proficiencyBonus" : character().stats.prof_bonus
	}
	feature = dump_json(attack)
	_ = [(feature:=feature.replace(f'{x}', str(subs[x]))) for x in ["intelligenceMod", "wisdomMod", "charismaMod", "proficiencyBonus"]]
	attack = load_json(feature)
	return attack

def messageText(cbt1, cbt2, args):
	returntext = ""
	if cbt1 and cbt2:	
		returntext += "'Transformation complete.\n\n"
		returntext += cbt1.name + " has been transformed into " + cbt2.name + "'\n\n"
	else:
		returntext += "'Transformation has been cancelled or failed.\n\n"
		returntext += "To avoid problems please respond with cancel - `c` - to the prompts that follow" + "'\n\n"
	return returntext

def getMetadata(cbt):
	c = combat()
	name = cbt.name
	transforms = load_json(c.get_metadata("transforms",{}))
	meta = transforms[name] if name in transforms else {}
	return meta
	
def setMetadata(cbt, newname):
	c = combat()
	transforms = load_json(c.get_metadata("transforms")) if c.get_metadata("transforms") else {}
	ownerid = cbt.controller
	transformkey = newname
	init = cbt.init
	monstername = cbt.monster_name if cbt.monster_name else "character"
	transforms[newname] = { "monster" : monstername , "owner" : ownerid , "init" : init, "name" : cbt.name, "hp" : cbt.hp }
	c.set_metadata("transforms",dump_json(transforms))
		
def moveInit(name):
	return f'''{ctx.prefix}init move "{name}"'''
