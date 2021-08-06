from tkinter import *
from PIL import ImageTk, Image
from boot import *
from math import ceil

window = Tk()
window.title("Shopping Center <<Python 2>>")
window.iconbitmap("images\icon.ico")
frame = Frame(window)

images = []


def addToCart(productId):
    global order
    global product
    global image_label
    global lName
    global lPriceAmount
    global lPriceCurrency

    print(f"Adding {productId} to cart!")

    product = prf.findById(productId)
    if product is None:
        print("No product with such ID found!")
    else:
        quantity = 1
        clientId = 1
        print(product.getPrice().amount)
        totalProProduct = product.getPrice().amount * quantity
        print(totalProProduct)
        order = orf.findByCustomerId(clientId)
        if order == None:
            order = orf.getOrder([], 0, clientId, 0)
        orderItem = oirf.getOrderItem(productId, quantity)
        print(orderItem.getItemId())
        order.addItem(orderItem.getItemId(), totalProProduct)
        print(order.getTotalCost())
        menubar.delete(2)

        menubar.add_command(label=f"Cart ({len(order.getItemList())}) Total {order.getTotalCost()}", command=renderCart)
    print(order)


def renderCatalog():
    global window
    global images
    global order
    global image_label
    global lName
    global lPriceAmount
    global lPriceCurrency
    global page



    prf.saveAll(jds.getProducts())
    products = prf.all()


    page = 0
    per_page = 5
    last_page = ceil(len(products) // per_page)
    frame.grid()
    status = Label(frame, text="Page 1 of " + str(last_page), bd=1, relief=SUNKEN, anchor=E)

    def productShow(page):
        global image_label
        global lName
        global lPriceAmount
        global lPriceCurrency
        row = 1
        for product in products:
            if page * per_page < product._id <= page * per_page + per_page :
                img = ImageTk.PhotoImage(Image.open(product.image_path))
                images.append(img)
                image_label = Label(frame, image=img, bg="white",  height=105, width=200)
                image_label.grid(row=row, column=0, columnspan=1)

                lName = Label(frame, text=product.name, bg="white", height=7, width=80, anchor=W)
                lName.grid(row=row, column=1, sticky=W)

                lPriceAmount = Label(frame, text=product.getPrice().amount, bg="white", height=7, width=5, anchor=W)
                lPriceAmount.grid(row=row, column=2)
                lPriceCurrency = Label(frame, text=product.getPrice().currency, bg="white", height=7, width=5, anchor=W)
                lPriceCurrency.grid(row=row, column=3)

                

                btnBuy = Button(frame, text="Add to Cart", bg="#6FF", height=6, width=9, anchor=W, command=lambda _id=product._id: addToCart(_id))
                btnBuy.grid(row=row, column=4)
                row += 1
                if row > per_page:
                    break

    productShow(page)

    def forward(image_number):
        global my_label, product
        global button_forward
        global button_back
        global image_label
        global lName
        global lPriceAmount
        global lPriceCurrency
        global page


        frame.grid_forget()
        frame.grid()
        button_forward = Button(frame, text=">>", command=lambda: forward(image_number + 1))
        button_back = Button(frame, text="<<", command=lambda: back(image_number - 1))
        page += 1
        productShow(page)

        if page + 1  == last_page:
            button_forward = Button(frame, text=">>", state=DISABLED)
        button_back.grid(row=6, column=0)
        button_forward.grid(row=6, column=2)

        status = Label(frame, text="Page " + str(page+1) + " of " + str(last_page), bd=1, relief=SUNKEN, anchor=E)
        status.grid(row=7, column=0, columnspan=5, sticky=W + E)

    def back(image_number):
        global button_forward
        global button_back
        global my_label, product
        global image_label
        global lName
        global lPriceAmount
        global lPriceCurrency
        global page


        frame.grid_forget()
        frame.grid()


        button_forward = Button(frame, text=">>", command=lambda: forward(image_number + 1))
        button_back = Button(frame, text="<<", command=lambda: back(image_number - 1))
        page -= 1
        productShow(page)

        if page == 0:
            button_back = Button(frame, text="<<", state=DISABLED)
        button_back.grid(row=6, column=0)
        button_forward.grid(row=6, column=2)

        status = Label(frame, text="Page " + str(page+1) + " of " + str(last_page), bd=1, relief=SUNKEN, anchor=E)
        status.grid(row=7, column=0, columnspan=5, sticky=W + E)
# ////
    button_back = Button(frame, text="<<", command=back, state=DISABLED)
    button_exit = Button(frame, text="Exit Program", command=window.quit)
    button_forward = Button(frame, text=">>", command=lambda: forward(2))

    button_back.grid(row=6, column=0)
    button_exit.grid(row=6, column=1)
    button_forward.grid(row=6, column=2, pady=10)
    status.grid(row=7, column=0, columnspan=5, sticky=W + E)


def renderCart():
    global window
    global order
    global product
    global lTotalCost
    global btnOrder
    global row
    frame.destroy()

    row = 0
    for item in order.getItemList():
        thing = prf.findById(item)
        lProductList = Label(window, text=thing, anchor=W, bg="white", height=5, width=80)
        lProductList.grid(row=row, columnspan=3, sticky=W)
        row += 1


    lTotalCost = Label(text=f" Total {order.getTotalCost()}", bg="white", bd=1, relief=SUNKEN, anchor=E, pady=10)
    lTotalCost.grid(row=row+1, columnspan=3, sticky=W + E)

    btnOrder = Button(text="Confirm Order & Pay", bg="red")
    btnOrder.grid(row=row+2, columnspan=3, sticky=E)


menubar = Menu(window)
menubar.add_command(label="Catalog", command=renderCatalog)
menubar.add_command(label="Cart (empty)", command=renderCart)
menubar.delete(2)
menubar.add_command(label="Cart (0)", command=renderCart)

window.config(menu=menubar)
window.mainloop()
