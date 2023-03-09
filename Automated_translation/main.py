import time

import polib
from googletrans import Translator
from tqdm import tqdm

# setting up performance timer
start_time = time.perf_counter()
# Initialize the Google Translate API
translator = Translator(service_urls=[
    'translate.google.com',
    'translate.google.co.kr',
])
# Load the PO file
po_file = polib.pofile('messages.po')

# Initialize exception count and success count
exception_count = 0
success_count = 0

# Iterate over the entries in the PO file
for entry in tqdm(po_file.untranslated_entries(), desc='Translating', total=len(po_file)):
    # Check if the entry has a source string
    if entry.msgid == '':
        exception_count += 1
        continue
    else:
        try:
            # Translate the source string to the target language
            translation = translator.translate(entry.msgid, dest='fr')

            # Check if the translation is None
            if translation is None:
                exception_count += 1
                continue

            # Set the translation as the new msgstr
            new_entry = polib.POEntry(
                msgid=entry.msgid,
                msgstr=translation.text,
                occurrences=entry.occurrences)
            po_file.append(new_entry)
            success_count += 1
        except TypeError:
            exception_count += 1
            continue
        except Exception as e:
            exception_count += 1
            print("error : %s " % e)

# Write the modified PO file back to disk
po_file.save()

# Print final status
total_actions = len(po_file)
percentage_success = success_count / total_actions * 100

print("Translation complete with %d exceptions" % exception_count)
print("Total actions: %d" % total_actions)
print("Successful translations: %d (%.2f%%)" % (success_count, percentage_success))
end_time = time.perf_counter()
sectoconvert = end_time - start_time
execution_time = time.strftime("%H:%M:%S", time.gmtime(sectoconvert))
print("The execution time is: %s" % execution_time)