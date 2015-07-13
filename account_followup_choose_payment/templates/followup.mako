<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>
    %for partner, level in partners_and_levels() :
    <% setLang(partner.lang) %>
    <% invoice_address = inv_address_by_partner(partner.id) %>
    <table style="width:100%;">
        <tr>
            <td><br/><br/><br/><br/><br/><br/><br/></td>
        </tr>
        <tr>
            <td>
            ${ partner.name|entity } <br/>
            ${ invoice_address and invoice_address.street or ''|entity } - ${ invoice_address and invoice_address.street2 or ''|entity } <br/>
            ${ invoice_address and invoice_address.zip or ''|entity} ${ invoice_address and invoice_address.city or ''|entity }<br/>
            ${ invoice_address and invoice_address.country_id and invoice_address.country_id.name or ''|entity }<br/>
            </td>    
        </tr>
        <tr>
            <td><br/><br/><br/><br/><br/></td>
        </tr>
        <tr>
            <td>
            ${_("Document: Customer account statement")}<br/>
            ${_("Date: ")} ${formatLang(fup_printing_date(partner.id, level.id), date=True)|entity}<br/>
            ${_("Customer Ref: ")} ${ partner.ref or ''|entity }<br/>
            </td>    
        </tr>
    </table>
    <table style="width:100%">
        <tr>    
            <td style="height: 50px;"></td>
        </tr>
        <tr>
            <td>${ message(partner.id, level.id) }</td>
        </tr>
        <tr>    
            <td style="height: 50px;"></td>
        </tr>
    </table>
<!--    <p>${ message(partner.id, level.id) }</p>-->
    <table style="width:100%" class="table_fup_lines">
        <thead style="border-bottom: solid">
            <tr>
                <th style="text-align:left">${_("Invoice Date")}</th>
                <th style="text-align:left">${_("Number")}</th>
                <th style="text-align:left">${_("Source Doc")}</th>
                <th style="text-align:left">${_("Maturity Date")}</th>
                <th style="text-align:right">${_("Currency")}</th>
                <th style="text-align:right">${_("Paid")}</th>
                <th style="text-align:right">${_("Due")}</th>
            </tr>
        </thead>
        <tbody>
            %for move_line in lines_by_partner_and_level(partner.id, level.id):
            <tr>
                <td style="text-align:left">${formatLang(move_line.invoice.date_invoice, date=True)|entity}</td>
                <td style="text-align:left">${move_line.invoice.number|entity}</td>
                <td style="text-align:left">${move_line.invoice.origin or ''|entity}</td>
                <td style="text-align:left">${formatLang(move_line.date_maturity or '', date=True)|entity}</td>
                <td style="text-align:right">${move_line.currency_id and move_line.currency_id.symbol or ''|entity} ${move_line.amount_currency and formatLang(move_line.amount_currency) or ''}</td>
                <td style="text-align:right">${move_line.reconcile_partial_id and partner.company_id.currency_id.symbol|entity} ${move_line.reconcile_partial_id and formatLang(line_amount_paid(move_line.reconcile_partial_id.id))}</td>
                <td style="text-align:right">${partner.company_id.currency_id.symbol|entity} ${formatLang(move_line.debit)}</td>
                <!--<td style="text-align:right">${move_line.reconcile_partial_id and partner.company_id.currency_id.symbol|entity} ${move_line.reconcile_partial_id and formatLang(line_amount_paid(move_line.reconcile_partial_id.id))}</td>-->
            </tr>
            %endfor
        </tbody>
        <tfoot>
            <tr>
                <td colspan="4"></td>
                <td colspan="2" style="border-top:1px solid #000">${_("Balance: ")}</td>
                <td style="text-align:right; border-top:1px solid #000">${partner.company_id.currency_id.symbol|entity} ${formatLang(partner_balance(partner.id, level.id))}</td>
                <td></td>
            </tr>
        </tfoot>
    </table>
    <table style="width:100%;">
        <tr>    
            <td style="height: 50px;"></td>
        </tr>
        <tr>
            <td>${ message2(partner.id, level.id) }</td>
        </tr>
        <tr>    
            <td style="height: 50px;"></td>
        </tr>
    </table>
     <p style="page-break-after:always; height: 1px !important;"></p>
    %endfor
</body>
</html>