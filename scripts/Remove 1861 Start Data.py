import os
import os.path
import shutil

def match_brace( text, start ):
    brace_count = 1 # we've counted the opening brace
    position = start + 1 # position after the brace
    
    while brace_count > 0:
        if position >= len( text ):
            print( text )
            raise "wtf"
        
        if text[ position ] == '{':
            brace_count += 1
        
        elif text[ position ] == '}':
            brace_count -= 1
            
        position += 1
        
    return position # the position after the matching closing brace

def remove_1861_data( file ):
    print( "Opening {}".format( file ) )
    text = ""
    
    with open( file ) as f:
        text = f.read()
        
        # Nothing found? Don't do anything
        if text.find( "1861" ) == -1:
            print( "    No 1861 scope" )
            return
    
    print( "    Removing 1861 scopes" )
    count = 0
    while True:
        section_start = text.find( "1861" )
        
        # no more? then we're done
        if section_start == -1:
            break
            
        brace_start = text.find( "{", section_start )
        
        end = match_brace( text, brace_start )
        
        # remove the section within the brace
        text = text[ 0 : section_start - 1 ] + text[ end : ]
        count += 1
        
        print( "        Replaced {} scope(s)".format( count ) )
    
    with open( file, 'w' ) as f:
        f.write( text )
        print( "    Writing result" )

def explore_folder( folder ):
    print( "Exploring {}".format( folder ) )
    
    for f in os.listdir( folder ):
        full_name = "{}\\{}".format( folder, f )
        
        if os.path.isfile( full_name ):
            remove_1861_data( full_name )
        else:
            explore_folder( full_name )

explore_folder( "..\\CTR\\history\\countries" )
explore_folder( "..\\CTR\\history\\provinces" )

print( "Removing 1861 pop history..." )
shutil.rmtree( "..\\CTR\\history\\pops\\1861.4.14" )
print( "    Complete" )

print( "Removing 1861 unit history..." )
shutil.rmtree( "..\\CTR\\history\\units\\1861" )
print( "    Complete" )
