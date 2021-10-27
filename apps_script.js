function logProductInfo() {
  var sheet = SpreadsheetApp.getActiveSheet();
  sheet.sort(4, false);

  var name = 'Markastok|Ürün Raporu'
  var file = DriveApp.getFilesByName(name);
  var mail = "okan@analyticahouse.com"
  MailApp.sendEmail(mail, "Cevat ARMUTLU", "Send Excel as PDF", {attachments: [file.next()]})
}