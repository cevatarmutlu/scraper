function logProductInfo() {
    var sheet = SpreadsheetApp.getActiveSheet();
    sheet.sort(4, false);

    var name = 'Markastok|Ürün Raporu_2021-10-27-01'
    var file = DriveApp.getFilesByName(name);
    var mail = "okan@analyticahouse.com"
    MailApp.sendEmail("cevatarmutlu@gmail.com", "Cevat ARMUTLU", "DENEME", {attachments: [file.next()]})
  }