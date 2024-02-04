from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Archive import Archive

from robocorp.tasks import task
from robocorp import browser


@task
def order_robots_from_RobotSpareBin():
    """
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    browser.configure(slowmo=100)
    open_robot_order_website()
    orders = get_orders()
    place_orders(orders)
    archive_receipts()



def open_robot_order_website():
    """Navigates to the given URL"""
    browser.goto("https://robotsparebinindustries.com/#/robot-order")


def get_orders():
    """ Download orders file from website and return Tables entity """
    http = HTTP()
    http.download(url='https://robotsparebinindustries.com/orders.csv', overwrite=True)

    library = Tables()
    orders = library.read_table_from_csv(
        "orders.csv", columns=["Order number", "Head", "Body", "Legs", "Address"]
    )
    return orders


def fill_the_form(order):
    page = browser.page()
    page.select_option("#head", str(order["Head"]))
    page.click(f"#id-body-{order['Body']}")
    page.fill("input.form-control", order["Legs"])
    page.fill("#address", str(order["Address"]))
    page.click("#order")


def close_annoying_modal():
    page = browser.page()
    page.click("button:text('OK')")


def check_errors() -> bool:
    error = browser.page().is_visible('div.alert.alert-danger')
    if error:
        return True
    else:
        return False


def store_order_as_pdf(order_number) -> str:
    """Export the data to a pdf file"""
    page = browser.page()
    sales_results_html = page.locator("#order-completion").inner_html()

    pdf = PDF()
    path_to_save = f"output/receipts/order_{order_number}.pdf"
    pdf.html_to_pdf(sales_results_html, path_to_save)
    return path_to_save


def place_orders(orders) -> None:
    for order in orders:
        close_annoying_modal()
        fill_the_form(order)

        while True:
            page = browser.page()
            if not check_errors():
                order_number = order['Order number']
                pdf_file = store_order_as_pdf(order_number)
                screenshot = screenshot_robot(order_number)

                embed_screenshot_to_receipt(screenshot, pdf_file)

                page.click("#order-another")
                break
            else:
                page.click("#order")


def screenshot_robot(order_number) -> str:
    """Take a screenshot of the page"""
    page = browser.page()
    path_to_save = f"output/receipts/screenshots/order_{order_number}.png"
    page.screenshot(path=path_to_save)
    return path_to_save


def embed_screenshot_to_receipt(screenshot: str, pdf_file: str) -> None:
    """
    :param screenshot: path_to_file
    :param pdf_file: path_to_file
    :return: None
    """

    pdf = PDF()
    file = [f'{screenshot}:align=center',]

    pdf.add_files_to_pdf(
        files=file,
        target_document=f"{pdf_file}", append=True
    )


def archive_receipts() -> None:
    """
    Create a ZIP file of receipt PDF files
    :return: None
    """
    lib = Archive()
    lib.archive_folder_with_zip('output/receipts', 'mydocs.zip', include='*.pdf')



















