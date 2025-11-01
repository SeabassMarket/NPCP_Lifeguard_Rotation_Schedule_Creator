/**
 * NPCP Lifeguard Scheduler - Main Apps Script Code
 * Modular, clean code following snake_case conventions
 */

// ============================================================================
// CONFIGURATION
// ============================================================================

// Template spreadsheet ID - replace with your actual template ID
const TEMPLATE_SPREADSHEET_ID = '1HouH8uW5hETBi7U-q5bm1rX3Fzfxip3GPzHwed6HL-s';

// ============================================================================
// MAIN WEB APP HANDLER
// ============================================================================

/**
 * Main function to serve the HTML page
 */
function doGet() {
  return HtmlService.createTemplateFromFile('index')
    .evaluate()
    .setTitle('NPCP Lifeguard Scheduler')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

/**
 * Include HTML files for modular structure
 */
function include(filename) {
  return HtmlService.createHtmlOutputFromFile(filename).getContent();
}

// ============================================================================
// TEMPLATE OPERATIONS
// ============================================================================

/**
 * Create a copy of the template spreadsheet
 * @return {Object} Template copy information
 */
function create_template_copy() {
  try {
    const template_file = DriveApp.getFileById(TEMPLATE_SPREADSHEET_ID);

    const now = new Date();

    // Array of month names
    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                        "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"];

    // Function to get the correct day suffix automatically
    function getDaySuffix(day) {
      if (day >= 11 && day <= 13) return "th"; // special case
      switch (day % 10) {
        case 1: return "st";
        case 2: return "nd";
        case 3: return "rd";
        default: return "th";
      }
    }

    const day = now.getDate();
    const formattedDate = `${monthNames[now.getMonth()]} ${day}${getDaySuffix(day)}, ${now.getFullYear()}`;
    const formattedTime = Utilities.formatDate(now, Session.getScriptTimeZone(), "HH:mm:ss");

    // Automatically generate the full name
    const copy_name = `${formattedDate} - NPCP Schedule Info - ${formattedTime}`;

    const copied_file = template_file.makeCopy(copy_name);
    const copied_spreadsheet = SpreadsheetApp.openById(copied_file.getId());

    return {
      status: 'success',
      data: {
        id: copied_file.getId(),
        name: copy_name,
        url: copied_spreadsheet.getUrl()
      }
    };
  } catch (error) {
    console.error('Error creating template copy:', error);
    return {
      status: 'error',
      message: 'Failed to create template copy: ' + error.message
    };
  }
}

// ============================================================================
// GOOGLE SHEETS OPERATIONS
// ============================================================================

/**
 * Get all accessible spreadsheets for the user
 * @return {Array} Array of spreadsheet objects with id and name
 */
function get_user_spreadsheets() {
  try {
    const files = DriveApp.getFilesByType(MimeType.GOOGLE_SHEETS);
    const spreadsheets = [];

    while (files.hasNext()) {
      const file = files.next();
      spreadsheets.push({
        id: file.getId(),
        name: file.getName()
      });
    }

    return {
      status: 'success',
      data: spreadsheets.sort((a, b) => a.name.localeCompare(b.name))
    };
  } catch (error) {
    console.error('Error getting spreadsheets:', error);
    return {
      status: 'error',
      message: 'Failed to retrieve spreadsheets: ' + error.message
    };
  }
}

/**
 * Get all accessible spreadsheets for output selection (same as get_user_spreadsheets but separate for clarity)
 * @return {Array} Array of spreadsheet objects with id and name
 */
function get_user_spreadsheets_for_output() {
  return get_user_spreadsheets();
}

/**
 * Read data from selected spreadsheet and get API response
 * @param {string} spreadsheet_id - The ID of the spreadsheet to read
 * @param {string} call - The type of API call ("preview" or "calculate")
 * @return {Object} API response data
 */
function read_spreadsheet_data(spreadsheet_id, call) {
  try {
    const spreadsheet = SpreadsheetApp.openById(spreadsheet_id);
    const sheets = spreadsheet.getSheets();

    const allSheetsData = sheets.map(sheet => {
      const values = sheet.getDataRange().getValues().filter(row => row.some(cell => cell !== ""));
      return {
        sheet_name: sheet.getName(),
        values: values,
        num_rows: values.length,
        num_cols: values.length > 0 ? values[0].length : 0
      };
    });

    const payload = {
      call: call,
      spreadsheet_name: spreadsheet.getName(),
      sheets: allSheetsData
    };

    const apiUrl = 'https://npcp-scheduler-api-64468458314.us-east4.run.app/read_data';
    const options = {
      method: 'post',
      contentType: 'application/json',
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    };

    const response = UrlFetchApp.fetch(apiUrl, options);
    const responseData = JSON.parse(response.getContentText());

    // Return the API response directly for processing on client side
    if (responseData.status === 'error') {
      return {
        status: 'error',
        message: responseData.message || 'Unknown error from API'
      };
    }

    return {
      status: 'success',
      data: {
        spreadsheet_name: spreadsheet.getName(),
        api_response: responseData
      }
    };

  } catch (error) {
    Logger.log('Error reading spreadsheet: %s', error);
    return {
      status: 'error',
      message: 'Failed to read spreadsheet: ' + error.message
    };
  }
}

/**
 * Create a new spreadsheet or get existing one
 * @param {string} spreadsheet_name - Name for new spreadsheet or existing one
 * @param {boolean} create_new - Whether to create new spreadsheet
 * @param {string} existing_id - ID of existing spreadsheet (optional)
 * @return {Object} Spreadsheet information
 */
function prepare_output_spreadsheet(spreadsheet_name, create_new, existing_id) {
  try {
    let spreadsheet;

    if (create_new) {
      spreadsheet = SpreadsheetApp.create(spreadsheet_name);
    } else if (existing_id) {
      // Use the provided spreadsheet ID
      spreadsheet = SpreadsheetApp.openById(existing_id);
    } else {
      // Try to find existing spreadsheet by name (fallback)
      const files = DriveApp.getFilesByName(spreadsheet_name);
      if (files.hasNext()) {
        const file = files.next();
        spreadsheet = SpreadsheetApp.openById(file.getId());
      } else {
        // If not found, create new one
        spreadsheet = SpreadsheetApp.create(spreadsheet_name);
      }
    }

    return {
      status: 'success',
      data: {
        id: spreadsheet.getId(),
        name: spreadsheet.getName(),
        url: spreadsheet.getUrl()
      }
    };
  } catch (error) {
    console.error('Error preparing output spreadsheet:', error);
    return {
      status: 'error',
      message: 'Failed to prepare output spreadsheet: ' + error.message
    };
  }
}

/**
 * Convert time string to minutes for sorting
 * @param {string} timeStr - Time string like "09:20 AM"
 * @return {number} Minutes since midnight
 */
function parseTimeToMinutes(timeStr) {
  if (!timeStr || timeStr === '-') return Infinity;

  const [time, meridian] = timeStr.split(' ');
  let [hours, minutes] = time.split(':').map(Number);

  if (meridian === 'PM' && hours !== 12) hours += 12;
  if (meridian === 'AM' && hours === 12) hours = 0;

  return hours * 60 + minutes;
}

/**
 * Convert a column number to its letter (A → 1, AA → 27, etc.)
 * @param {number} num - Column number (1-based index)
 * @return {string} - Column letter
 */
function numberToColumnLetter(num) {
  let letters = "";
  while (num > 0) {
    let remainder = (num - 1) % 26;
    letters = String.fromCharCode(65 + remainder) + letters;
    num = Math.floor((num - 1) / 26);
  }
  return letters;
}

/**
 * Write schedule data to spreadsheet in table format
 * @param {string} spreadsheet_id - Target spreadsheet ID
 * @param {Object} schedule_data - Schedule data from API
 * @param {Array} lifeguards - Array of lifeguard names
 * @param {boolean} create_new - Whether this is a new spreadsheet
 * @return {Object} Write operation result
 */
function write_schedule_to_spreadsheet(spreadsheet_id, schedule_data, lifeguards, create_new, upStandNames) {
  try {
    const spreadsheet = SpreadsheetApp.openById(spreadsheet_id);
    const tz = Session.getScriptTimeZone();
    const timestamp = Utilities.formatDate(new Date(), tz, "MM/dd/yy (HH:mm:ss)");
    const sheetName = `Lifeguard Schedule - ${timestamp}`;

    let sheet;
    if (create_new) {
      // Rename the active sheet and force it to position 1
      sheet = spreadsheet.getActiveSheet().setName(sheetName);
      sheet.activate();
      spreadsheet.moveActiveSheet(1);
    } else {
      // Insert at index 1, then force-move as a reliable fallback
      sheet = spreadsheet.insertSheet(sheetName, 1);
      sheet.activate();
      spreadsheet.moveActiveSheet(1);
    }

    // Clear existing content
    sheet.clear();

    // Get and sort times
    const times = Object.keys(schedule_data).filter(time => time !== 'Lifeguards');
    times.sort((a, b) => parseTimeToMinutes(a) - parseTimeToMinutes(b));

    // Add indices to the lifeguard names
    for (let i = 0; i < lifeguards.length; i++){
      lifeguards[i] = `${i + 1}. ${lifeguards[i]}`
    }

    // Create header row: empty cell + lifeguard names
    const headerRow = ['', ...lifeguards];

    // Create data rows
    const dataRows = times.map(time => {
      const timeSlot = schedule_data[time];
      const row = [time];

      // Add assignments for each lifeguard position
      for (let i = 0; i < lifeguards.length; i++) {
        const assignment = timeSlot[i];
        row.push(assignment === null ? '' : assignment);
      }

      return row;
    });

    // Combine header and data
    const allData = [headerRow, ...dataRows];

    // Duplicate initial at the end
    for (let i = 0; i < allData.length; i++){
      let newTimeStr = allData[i][0]
      newTimeStr = newTimeStr.substring(0, 5)
      if(newTimeStr.substring(0, 1) === "0"){
        newTimeStr = newTimeStr.substring(1)
      }

      allData[i][0] = `'${newTimeStr}`

      allData[i].push(allData[i][0])
    }

    const ROW_START = 3
    const COLUMN_START = 1

    // ============================================================
    // WRITE TO SHEET
    // ============================================================
    if (allData.length > 0) {

      // ==============================
      // Get info in
      // ==============================

      const range = sheet.getRange(ROW_START, COLUMN_START, allData.length, allData[0].length);
      range.setValues(allData);

      // Freeze header row
      sheet.setFrozenRows(ROW_START);

      // Freeze time column
      sheet.setFrozenColumns(COLUMN_START);

      // ==============================
      // General formatting
      // ==============================

      sheet.setRowHeight(ROW_START, 80);

      sheet.setColumnWidths(1, sheet.getMaxColumns(), 35);

      sheet.setColumnWidths(COLUMN_START + 1, allData[0].length - 2, 25);

      sheet.getRange(1, 1, sheet.getMaxRows(), sheet.getMaxColumns())
        .setFontFamily("Times New Roman")
        .setFontSize(10);

      // ==============================
      // BORDERS
      // ==============================

      sheet.getRange(ROW_START + 1, COLUMN_START + 1, allData.length - 1, allData[0].length - 2).setBorder(
        false,
        false,
        false,
        false,
        true,
        true,
        "black",
        SpreadsheetApp.BorderStyle.SOLID
      );

      sheet.getRange(ROW_START, COLUMN_START, 1, allData[0].length).setBorder(
        false,
        false,
        true,
        false,
        true,
        false,
        "black",
        SpreadsheetApp.BorderStyle.SOLID_MEDIUM
      )

      sheet.getRange(ROW_START + 1, COLUMN_START, allData.length - 1, 1).setBorder(
        true,
        false,
        true,
        true,
        false,
        false,
        "black",
        SpreadsheetApp.BorderStyle.SOLID_MEDIUM
      ).setHorizontalAlignment("right")

      sheet.getRange(ROW_START + 1, COLUMN_START + allData[0].length - 1, allData.length - 1, 1).setBorder(
        true,
        true,
        true,
        false,
        false,
        false,
        "black",
        SpreadsheetApp.BorderStyle.SOLID_MEDIUM
      )

      sheet.getRange(ROW_START + allData.length, COLUMN_START, 1, allData[0].length).setBorder(
        true,
        false,
        true,
        false,
        true,
        false,
        "black",
        SpreadsheetApp.BorderStyle.SOLID_MEDIUM
      )

      sheet.getRange(1, 1, 1, 9).setBorder(
        false,
        false,
        true,
        false,
        false,
        false,
        "black",
        SpreadsheetApp.BorderStyle.SOLID_MEDIUM
      )

      // ==============================
      // Top
      // ==============================

      for (let i = COLUMN_START + 1; i < COLUMN_START + allData[0].length - 1; i += 2){
        const letters = numberToColumnLetter(i)

        sheet.getRange(`${letters}${ROW_START}:${letters}`).setBackground('#00CCFF');
      }

      sheet.getRange(ROW_START, 1, 1, sheet.getMaxColumns()).setTextRotation(45)

      sheet.getRange(ROW_START, COLUMN_START + 1, sheet.getMaxRows(), allData[0].length - 2).setHorizontalAlignment("center");

      // ==============================
      // Stands
      // ==============================

      // For each column
      for (let c = 1; c < allData[0].length - 1; c++){

        let lastStand = 1

        // Check each row (value in the column)
        for (let r = 1; r < allData.length; r++){

          // Get values
          const dataValue = allData[r][c]
          const previousDataValues = allData[r - 1]
          let nextDataValues;

          if (r < allData.length - 1) {
            nextDataValues = allData[r + 1];
          } else {
            nextDataValues = [];
          }

          // Color breaks
          if(dataValue === "BREAK"){
            sheet.getRange(ROW_START + r, COLUMN_START + c, 2, 1).setValue("").setBackground("#FFFF00");
            r += 1

          } else if (dataValue in upStandNames && !(previousDataValues.includes(dataValue)) && !(nextDataValues.includes(dataValue))){
            sheet.getRange(ROW_START + r, COLUMN_START + c, 1, 1).setBackground("#FF7F00");

          } else if (dataValue in upStandNames && !(previousDataValues.includes(dataValue))){
            sheet.getRange(ROW_START + r, COLUMN_START + c, 1, 1).setBackground("#00FF00");

          } else if (dataValue in upStandNames && !(nextDataValues.includes(dataValue))){
            sheet.getRange(ROW_START + r, COLUMN_START + c, 1, 1).setBackground("#FF0000");

          }

          if(dataValue.length > 0){
            lastStand = r
          }
        }

        // Add grayed out tail
        const amountOfGrayedBoxes = allData.length - lastStand - 1
        if (amountOfGrayedBoxes > 0){
          sheet.getRange(ROW_START + lastStand + 1, COLUMN_START + c, amountOfGrayedBoxes, 1).setBackground("#999999");
        }
      }

      // ==============================
      // Header (Day and date)
      // ==============================

      // Day
      sheet.getRange(1, 1, 1, 1).setValue("Day:").setHorizontalAlignment("left").setFontWeight("bold")

      sheet.getRange("B1:D1").merge();

      const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

      const today = new Date();
      const dayName = days[today.getDay()];
      sheet.getRange(1, 2, 1, 1).setValue(dayName).setHorizontalAlignment("center")

      // Date
      sheet.getRange("E1:F1").merge();

      sheet.getRange(1, 5, 1, 1).setValue("Date:").setHorizontalAlignment("left").setFontWeight("bold")

      sheet.getRange("G1:I1").merge();

      const date = Utilities.formatDate(today, tz, "MM/dd/yy");
      sheet.getRange(1, 7, 1, 1).setValue(date).setHorizontalAlignment("center")
    }

    return {
      status: 'success',
      data: {
        rows_written: allData.length,
        cols_written: allData.length > 0 ? allData[0].length : 0,
        sheet_name: sheet.getName(),
        url: spreadsheet.getUrl()
      }
    };
  } catch (error) {
    console.error('Error writing to spreadsheet:', error);
    return {
      status: 'error',
      message: 'Failed to write to spreadsheet: ' + error.message
    };
  }
}

/**
 * Write data to spreadsheet (legacy function for compatibility)
 * @param {string} spreadsheet_id - Target spreadsheet ID
 * @param {Array} data - 2D array of data to write
 * @return {Object} Write operation result
 */
function write_to_spreadsheet(spreadsheet_id, data) {
  try {
    const spreadsheet = SpreadsheetApp.openById(spreadsheet_id);
    const sheet = spreadsheet.getActiveSheet();

    // Clear existing content
    sheet.clear();

    // Write new data
    if (data && data.length > 0) {
      const range = sheet.getRange(1, 1, data.length, data[0].length);
      range.setValues(data);
    }

    return {
      status: 'success',
      data: {
        rows_written: data.length,
        url: spreadsheet.getUrl()
      }
    };
  } catch (error) {
    console.error('Error writing to spreadsheet:', error);
    return {
      status: 'error',
      message: 'Failed to write to spreadsheet: ' + error.message
    };
  }
}

// ============================================================================
// MAIN PROCESSING WORKFLOW
// ============================================================================

/**
 * Main function to process the lifeguard scheduling
 * @param {string} input_spreadsheet_id - Input spreadsheet ID
 * @param {string} output_name - Output spreadsheet name
 * @param {boolean} create_new - Whether to create new output spreadsheet
 * @param {string} existing_output_id - ID of existing output spreadsheet (optional)
 * @return {Object} Processing result with output spreadsheet info
 */
function process_lifeguard_schedule(input_spreadsheet_id, output_name, create_new, existing_output_id) {
  try {
    // Step 1: Read input data and call API
    const input_result = read_spreadsheet_data(input_spreadsheet_id, "calculate");
    if (input_result.status !== 'success') {
      return input_result;
    }

    // Extract the schedule data and lifeguards from API response
    const api_response = input_result.data.api_response;
    if (!api_response || !api_response.response || !api_response.response.Schedule || !api_response.response.Lifeguards) {
      return {
        status: 'error',
        message: 'Invalid API response format - missing Schedule or Lifeguards data'
      };
    }

    const schedule_data = api_response.response.Schedule;
    const lifeguards = api_response.response.Lifeguards;
    const upStandNames = api_response.response['Up Stands'];

    // Step 2: Prepare output spreadsheet
    const output_prep_result = prepare_output_spreadsheet(output_name, create_new, existing_output_id);
    if (output_prep_result.status !== 'success') {
      return output_prep_result;
    }

    // Step 3: Write schedule to output spreadsheet
    const write_result = write_schedule_to_spreadsheet(
      output_prep_result.data.id,
      schedule_data,
      lifeguards,
      create_new,
      upStandNames
    );

    if (write_result.status !== 'success') {
      return write_result;
    }

    // Step 4: Return success with output info
    return {
      status: 'success',
      data: {
        output_spreadsheet: {
          id: output_prep_result.data.id,
          name: output_prep_result.data.name,
          url: output_prep_result.data.url
        },
        processing_summary: {
          total_times: Object.keys(schedule_data).length - 1, // -1 for Lifeguards key
          total_lifeguards: lifeguards.length,
          rows_written: write_result.data.rows_written,
          cols_written: write_result.data.cols_written,
          sheet_name: write_result.data.sheet_name
        }
      }
    };

  } catch (error) {
    console.error('Error in main processing workflow:', error);
    return {
      status: 'error',
      message: 'Processing failed: ' + error.message
    };
  }
}