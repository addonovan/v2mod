import re
from os.path import isfile

r_invention = re.compile( '^([a-zA-z]*?) = {' )
r_rename = re.compile( '\$NAME\$' )

nonmilitary_modifier = "\tmodifier = { factor = 2  any_neighbor_country = { invention = $NAME$ } }\n"
military_modifier = "\tmodifier = { factor = 1  war = yes  any_greater_power = { war_with = THIS } }\n"

def is_block_start( text ):
	result = r_invention.search( text )
	return result

def match_brace( text ):
	block = ""
	brace_count = 0

	while brace_count > 0 or len( block ) == 0:
		open_index = text.find( "{" )
		close_index = text.find( "}" )

		until_index = 0

		if open_index == -1 and close_index == -1:
			raise ValueError( "Could not find any matching brace!" )

		if ( open_index < close_index or close_index == -1 ) and open_index != -1:
			brace_count += 1
			until_index = open_index

		elif ( close_index < open_index or open_index == -1 ) and close_index != -1:
			brace_count -= 1
			until_index = close_index

		substring = text[ 0 : until_index + 1 ] # make sure we grab the brace
		block += substring
		text = text[ len( substring ) : ]

	return block

def add_modifier( name, block, modifier ):
	# find just the chance block
	chance_index = block.find( "chance = {" )
	pre_chance = block[ 0 : chance_index ]
	chance = match_brace( block[ chance_index : ] )[ : - 1 ] # match the braces for the chance section, but remove ending brace
	post_chance = block[ len( pre_chance ) + len( chance ) : ] # grab the stuff after

	# insert our modifier
	chance += modifier + "\t"

	return pre_chance + r_rename.sub( name, chance ) + post_chance

def search_file( file, modifier ):
	with open( file ) as f:
		content = f.read();

	output = ""

	while "\n" in content:
		line = content[ 0 : content.find( "\n" ) ] # grab the current line

		result = is_block_start( line )

		if result:
			name = result.group( 1 )
			block = match_brace( content )
			output += add_modifier( name, block, modifier )
			
			content = content[ len( block ) + 1 : ]

		else:
			output += line
			content = content[ len( line ) + 1 : ]

		output += "\n"		

	return output


folder = "../CTR/inventions/"
name = ""

while True:
	name = input( "Name of the file? " )
	file = folder + name

	if isfile( file ):

		# default to the nonmilitary invention modifier
		modifier = nonmilitary_modifier

		# if the user says that these are military techs, then change the modifier
		if input( "Are these military techs? (y/n)  " )[ 0 ] == 'y':
			modifier = military_modifier

		print( "Parsing {}".format( file ) )
		content = search_file( file, modifier )

		print( "Updating file" )
		with open( file, 'w+' ) as f:
			f.write( content )

		print( "" )

	else:
		print( "That's not an existing file" )
		break

	# Print new lines for prettification
	print( "\n\n\n" )