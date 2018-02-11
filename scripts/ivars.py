"""Print out all the ivars of an object.

NOTE: The parsing of the ivar type encoding is very hacky, but it should
       be sufficient for most cases. Therefore the resulting list may have
       mistakes or could be missing some ivars whose type could not be parsed.

Usage: ivars <object>
"""
import lldb
import shlex

from subprocess import call

def ivars(debugger, command, result, internal_dict):
  args = shlex.split(command)
  if len(args) != 1:
    print 'ERROR: Please enter the command as "ivars <object>".'
    return

  cmd = """
    @import Foundation;
    @import ObjectiveC;

    NSMutableArray *ivarStrings = [NSMutableArray array];
    unsigned int count;
    Ivar *ivars = class_copyIvarList((Class)[(id){0} class], &count);
    for (int i = 0; i < count; i++) {{
      Ivar ivar = ivars[i];
      const char *ivarName = ivar_getName(ivar);
      NSString *name = [NSString stringWithFormat: @"%s", ivarName];

      //////////////////////////////////////////////////////////////////////////////////////
      // Decode ivar type. Since LLDB does not allow defining functions, I'm inlining all //
      // of the code here.                                                                //
      //////////////////////////////////////////////////////////////////////////////////////
      NSString *typeEncoding = [NSString stringWithUTF8String:ivar_getTypeEncoding(ivar)];
      NSDictionary *basicTypes = @{{
        @"c" : @"char (or BOOL)",
        @"i" : @"int",
        @"s" : @"short",
        @"l" : @"long",
        @"q" : @"long long",
        @"C" : @"unsigned char",
        @"I" : @"unsinged int",
        @"S" : @"unsigned short",
        @"L" : @"unsigned long",
        @"Q" : @"unsigned long long",
        @"f" : @"float",
        @"d" : @"double",
        @"B" : @"bool",
        @"v" : @"void",
        @"*" : @"char *",
        @"#" : @"Class",
        @":" : @"SEL"
      }};

      NSMutableString *finalEncoding = [NSMutableString string];
      for (NSUInteger j = 0; j < typeEncoding.length; j++) {{
        unichar c = [typeEncoding characterAtIndex:j];

        // Primitive types
        NSString *type = [basicTypes objectForKey:[NSString stringWithFormat:@"%c", c]];
        if (type) {{
          [finalEncoding insertString:type atIndex:0];
        }}

        // Objective-C objects
        if (c == '@') {{
          if ((typeEncoding.length-1 > j) && ([typeEncoding characterAtIndex:1] == '"')) {{
            j++;  // Consume the opening parenthesis.
            unichar nextChar = [typeEncoding characterAtIndex:++j];
            while (nextChar != '"') {{
              [finalEncoding appendFormat:@"%c", nextChar];
              nextChar = [typeEncoding characterAtIndex:++j];
            }}
            [finalEncoding appendString:@" *"];
            break;
          }}
          [finalEncoding insertString:@"id" atIndex:0];
        }}

        // Arrays
        if (c == '[') {{
          unichar nextChar = [typeEncoding characterAtIndex:++j];
          NSMutableString *arraySize = [NSMutableString stringWithString:@"["];
          while (isdigit(nextChar)) {{
            [arraySize appendFormat:@"%c", nextChar];
            nextChar = [typeEncoding characterAtIndex:++j];
          }}
          j--;  // Manual correct to the index.
          [finalEncoding appendFormat:@"%@]", arraySize];
        }}

        // Structs and Unions
        if (c == '{{' || c == '(') {{
          unichar nextChar = [typeEncoding characterAtIndex:++j];
          NSMutableString *structureName = [NSMutableString string];
          while(nextChar != '=') {{
            [structureName appendFormat:@"%c", nextChar];
            nextChar = [typeEncoding characterAtIndex:++j];
          }}
          NSString *structureType = (c == '{{') ? @"struct" : @"union";
          [finalEncoding insertString:[NSString stringWithFormat:@"%@ %@", structureType, structureName]
                              atIndex:0];
          break;  // Don't traverse their types. It's too verbose.
        }}

        // Const keyword
        if (c == 'r') {{
          if (finalEncoding.length && ([finalEncoding characterAtIndex:finalEncoding.length-1] != '*')) {{
            [finalEncoding appendString:@" "];
          }}
          [finalEncoding appendString:@" const "];
        }}

        // Pointers
        if (c == '^') {{
          [finalEncoding appendString:@"*"];
        }}

        // "Unknown" meaning function pointer, block, or other.
        if (c == '?') {{
          if (j == 0) {{
            continue;
          }}
          unichar previousChar = [typeEncoding characterAtIndex:(j - 1)];
          if (previousChar == '^') {{
            finalEncoding = [NSMutableString stringWithString:@"~function pointer~"];
            break;
          }}
          if (previousChar == '@') {{
            finalEncoding = [NSMutableString stringWithString:@"~block~"];
            break;
          }}
        }}
      }}
      //////////////////////////////////////////////////////////////////////////////////////
      // End function.                                                                    //
      //////////////////////////////////////////////////////////////////////////////////////

      if ([typeEncoding characterAtIndex:0] == '@') {{
        id object = object_getIvar((id){0}, ivar);
        if (object) {{
          [ivarStrings addObject:[NSString stringWithFormat:@"(%@) %@ -> %p", finalEncoding, name, object]];
        }} else {{
          [ivarStrings addObject:[NSString stringWithFormat:@"(%@) %@ -> nil", finalEncoding, name]];
        }}
        continue;
      }}
      [ivarStrings addObject:[NSString stringWithFormat:@"(%@) %@", finalEncoding, name]];
    }}
    free(ivars);
    ivarStrings;  // Return the list of ivar strings as an NSArray.
  """.format(args[0])
  target = debugger.GetSelectedTarget()
  if target is None:
    print 'ERROR: Could not get selected target.'
    return
  ret_value = target.EvaluateExpression(cmd)
  if ret_value is None:
    print 'ERROR: Invalid return value from expression: ' + cmd
    return
  if not ret_value.GetError().Success():
    print ret_value.GetError()
    return
  ivar_array = ret_value.GetObjectDescription()
  if ivar_array is None:
    print 'ERROR: Could not parse ivars for object (' + args[0] + ')'
    return
  print ivar_array

def __lldb_init_module(debugger, internal_dict):
  debugger.HandleCommand('command script add -f ivars.ivars ivars')
