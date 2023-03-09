import asyncio
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
po_file = polib.pofile('messages_last-v2.po')
# Initialize exception count and success count
exception_count = 0
success_count = 0


# Define the translation coroutine
async def translate_entry(entry):
    try:
        # Translate the source string to the target language
        translation = await asyncio.get_event_loop().run_in_executor(None, translator.translate, entry.msgid, 'fr')

        # Set the translation as the new msgstr
        new_entry = polib.POEntry(
            msgid=entry.msgid,
            msgstr=translation.text,
            occurrences=entry.occurrences)
        po_file.append(new_entry)
        return True
    except Exception as e:
        print("error : %s " % e)
        return False


# Define the main coroutine
async def main(success_count, exception_count):
    # Iterate over the entries in the PO file
    for entry in tqdm(po_file.untranslated_entries(), desc='Translating', total=len(po_file)):
        # Check if the entry has a source string
        if entry.msgid == '':
            exception_count += 1
            continue
        else:
            # Check if the msgstr is empty
            if not entry.msgstr:
                # Translate the entry asynchronously
                success = await translate_entry(entry)
                if success:
                    success_count += 1
                else:
                    exception_count += 1
            else:
                continue


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

# Run the main coroutine
asyncio.run(main(success_count, exception_count))
