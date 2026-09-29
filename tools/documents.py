"""Certificate documents: verbatim transcriptions and key facts, exactly as printed on the
scanned documents in legacy/original-site/. Do not edit values without the source image."""

# ---------------------------------------------------------------- certificate transcriptions (verbatim, as printed)
TRANSCRIPT = {
"air-agency-certificate": """
<p class="centered">UNITED STATES OF AMERICA<br>DEPARTMENT OF TRANSPORTATION<br>FEDERAL AVIATION ADMINISTRATION</p>
<p class="centered"><strong>Air Agency Certificate</strong><br>Number <strong>V9DR072Y</strong></p>
<p>This certificate is issued to <strong>CONFIDENCE AVIATION INC.</strong> whose business address is 7605 N.W. 50TH STREET, MIAMI, FLORIDA 33166 upon finding that its organization complies in all respects with the requirements of the Federal Aviation Regulations relating to the establishment of an Air Agency, and is empowered to operate an approved REPAIR STATION with the following ratings:</p>
<p class="centered"><strong>RADIO (June 13, 2000)</strong><br><strong>LIMITED ACCESSORY (Nov 18, 1999)</strong></p>
<p>This certificate, unless canceled, suspended, or revoked, shall continue in effect INDEFINITELY.</p>
<p>Date issued: DECEMBER 15, 1998</p>
<p>By direction of the Administrator: MICHAEL C. THOMAS, MANAGER, SO-MIAMI FSDO-19</p>
<p>This Certificate is not Transferable, and any major change in the basic facilities, or in the location thereof, shall be immediately reported to the appropriate regional office of the Federal Aviation Administration.</p>
<p>Any alteration of this certificate is punishable by a fine of not exceeding $1,000, or imprisonment not exceeding 3 years, or both.</p>
<p>FAA Form 8000-4 (1-67) &nbsp; SUPERCEDES FAA FORM 395.</p>
""",
"easa-approval-certificate": """
<p class="centered">European Aviation Safety Agency</p>
<p class="centered"><strong>APPROVAL CERTIFICATE</strong><br>REFERENCE EASA.145.5139</p>
<p>Taking into account the provisions of Article 9(2) of Regulation (EC) No 1592/2002<sup><a href="#easa-legibility">*</a></sup> of the European Parliament and of the Council and the bilateral agreements currently in force between European Union Member States and the Government of the United States of America, the European Aviation Safety Agency (EASA) hereby certifies:</p>
<p class="centered"><strong>CONFIDENCE AVIATION INC.</strong><br>FAA Repair Station Number: V9DR072Y<br>7605 N.W. 50th Street<br>Miami, Florida 33166<br>USA</p>
<p>as a Part-145 maintenance organization approved to maintain the products listed in the FAA Air Agency Certificate and associated Operations Specifications and to issue related certificates of release to service using the above reference, subject to the following conditions:</p>
<ol>
<li>The scope of the approval is limited to that specified on the FAR Part 145 repair station Air Agency Certificate, and the associated Operations Specifications for work carried out in the USA (Unless otherwise agreed in a particular case by EASA).</li>
<li>This approval requires continued compliance with FAR Part 145 and the differences as specified in the Maintenance Implementation Procedures, including the use of the FAA Form 8130-3 for release/return to service of components up to and including powerplants.</li>
<li>Certificates of return to service must quote the EASA Part 145 approval reference number quoted above and the FAR Part 145 Air Agency Certificate number.</li>
<li>Subject to compliance with the foregoing conditions, this approval shall remain valid for an unlimited duration until the approval is surrendered, superseded, suspended or revoked.</li>
</ol>
<p>Date of issue: 19th October 2004<br>Signed — For EASA</p>
<p>EASA Form 3 &nbsp; Page 1 of 1</p>
<p class="note" id="easa-legibility">* The regulation number is partly illegible in the scanned document; see the document image.</p>
""",
"operations-specifications": """
<p>U.S. Department of Transportation — Federal Aviation Administration<br><strong>Operations Specifications</strong></p>
<p><strong>A003. Ratings and Limitations</strong> — HQ Control: 12/16/98 &nbsp; HQ Revision: 00c</p>
<p>The Certificate Holder is authorized the following Ratings and/or Limitations:</p>
<p><strong>Class Ratings</strong></p>
<ul><li>Radio Class 1: Communications Equipment</li><li>Radio Class 2: Navigational Equipment</li><li>Radio Class 3: Radar Equipment</li></ul>
<div class="table-wrap"><table><caption>Limited Ratings</caption>
<thead><tr><th scope="col">Rating</th><th scope="col">Manufacturer</th><th scope="col">Make / Model</th><th scope="col">Limitations</th></tr></thead>
<tbody><tr><td>Accessories</td><td>From the Approved Capabilities List</td><td>Current Revision</td><td>N/A</td></tr></tbody></table></div>
<div class="table-wrap"><table><caption>Limited Ratings - Specialized Services</caption>
<thead><tr><th scope="col">Rating</th><th scope="col">Specifications</th><th scope="col">Limitations</th></tr></thead>
<tbody><tr><td>None Authorized</td><td>N/A</td><td>N/A</td></tr></tbody></table></div>
<ol>
<li>Issued by the Federal Aviation Administration.</li>
<li>These Operations Specifications are approved by direction of the Administrator.<br>Schmidt, Gordon, Principal Avionics Inspector, SO19</li>
<li>Date Approval is effective: 1/22/03 &nbsp; Amendment Number: 2</li>
<li>I hereby accept and receive the Operations Specifications in this paragraph.<br>Hernandez, Alexis R., General Manager &nbsp; Date: 1/22/03</li>
</ol>
<p>Print Date: 1/28/2003 &nbsp; A003-1 &nbsp; Confidence Aviation, Inc. &nbsp; Certificate No.: V9DR072Y</p>
""",
}

SPEC = {  # key facts printed on each document; values verbatim, labels translated per language
"air-agency-certificate": [
    ("Issued by", "Emitido por", "United States of America, Department of Transportation, Federal Aviation Administration"),
    ("Certificate number", "Número de certificado", '<span class="mono">V9DR072Y</span>'),
    ("Issued to", "Emitido a", "CONFIDENCE AVIATION INC."),
    ("Business address", "Dirección comercial", "7605 N.W. 50th Street, Miami, Florida 33166"),
    ("Approved as", "Aprobado como", "REPAIR STATION"),
    ("Ratings", "Habilitaciones", "RADIO (June 13, 2000)<br>LIMITED ACCESSORY (Nov 18, 1999)"),
    ("Date issued", "Fecha de emisión", "DECEMBER 15, 1998"),
    ("Duration (as printed)", "Vigencia (según el documento)", "Unless canceled, suspended, or revoked, shall continue in effect INDEFINITELY"),
    ("Signed", "Firmado", "MICHAEL C. THOMAS, MANAGER, SO-MIAMI FSDO-19 (by direction of the Administrator)"),
    ("Form", "Formulario", "FAA Form 8000-4 (1-67), SUPERCEDES FAA FORM 395"),
],
"easa-approval-certificate": [
    ("Issued by", "Emitido por", "European Aviation Safety Agency (EASA)"),
    ("Reference", "Referencia", '<span class="mono">EASA.145.5139</span>'),
    ("Certifies", "Certifica a", "CONFIDENCE AVIATION INC."),
    ("FAA Repair Station Number", "Número de estación reparadora FAA", '<span class="mono">V9DR072Y</span>'),
    ("Address", "Dirección", "7605 N.W. 50th Street, Miami, Florida 33166, USA"),
    ("Approved as", "Aprobado como", "Part-145 maintenance organization"),
    ("Date of issue", "Fecha de emisión", "19th October 2004"),
    ("Duration (as printed)", "Vigencia (según el documento)", "Valid for an unlimited duration until the approval is surrendered, superseded, suspended or revoked, subject to the conditions listed"),
    ("Form", "Formulario", "EASA Form 3"),
],
"operations-specifications": [
    ("Issued by", "Emitido por", "U.S. Department of Transportation, Federal Aviation Administration"),
    ("Paragraph", "Párrafo", "A003. Ratings and Limitations"),
    ("HQ Control / HQ Revision", "HQ Control / HQ Revision", "12/16/98 / 00c"),
    ("Certificate No.", "Certificado No.", '<span class="mono">V9DR072Y</span>'),
    ("Class Ratings", "Habilitaciones de clase", "Radio Class 1: Communications Equipment<br>Radio Class 2: Navigational Equipment<br>Radio Class 3: Radar Equipment"),
    ("Limited Ratings", "Habilitaciones limitadas", "Accessories — From the Approved Capabilities List — Current Revision — Limitations: N/A"),
    ("Specialized Services", "Servicios especializados", "None Authorized"),
    ("Date approval is effective", "Fecha de vigencia de la aprobación", "1/22/03 (Amendment Number: 2)"),
    ("Approved by", "Aprobado por", "Schmidt, Gordon, Principal Avionics Inspector, SO19"),
    ("Accepted by", "Aceptado por", "Hernandez, Alexis R., General Manager (1/22/03)"),
    ("Print date / page", "Fecha de impresión / página", "1/28/2003 / A003-1"),
],
}


