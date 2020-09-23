import heapq as pq


class order_book:

    def __init__(self):
        self.next_order_id = 1
        self.order_book = {'ask': {}, 'bid': {}}
        self.max_heap = []
        self.min_heap = []
        self.price_to_order = {}
        self.fulfilled = set()

    # Adds Order to Book, increments order ID
    def add_limit_order(self, side, user_id, quantity, price):
        order_id = self.next_order_id
        self.order_book[side][self.next_order_id] = {'order_id': order_id, 'side': side, 'user_id': user_id,
                                                     'quantity': quantity, 'price': price}
        self.price_to_order[price] = order_id
        self.next_order_id += 1
        self.update_bbo_when_add(side, price)
        return order_id

    def place_market_order(self, side, quantity):
        qty_remain, total_price = self.update_bbo_when_market(side, quantity)
        qty_filled = quantity - qty_remain
        return [qty_filled, total_price / qty_filled]

    def maintain_heap_invariant(self):
        while self.max_heap != [] and self.max_heap[0] not in self.price_to_order:
            pq.heappop(self.max_heap)
        while self.min_heap != [] and self.min_heap[0] not in self.price_to_order:
            pq.heappop(self.min_heap)

    # Cancels order (removes from book), gives error messages if not possible
    def cancel_limit_order(self, order_id):
        if order_id in self.order_book['bid']:
            side = 'bid'
        elif order_id in self.order_book['ask']:
            side = 'ask'
        elif order_id in self.fulfilled:
            print('Order Fulfilled: Unable to Cancel')
            return
        else:
            print('Order not found -- please verify order ID')
            return
        price = self.order_book['side'][order_id]['price']
        self.order_book[side].pop(order_id)
        self.update_bbo_when_cancel(side, price)

    # Push new price onto appropriate heap upon adding new order
    def update_bbo_when_add(self, side, price):
        self.maintain_heap_invariant()
        if side == "ask":
            pq.heappush(self.min_heap, price)
        if side == "bid":
            pq.heappush(self.max_heap, -price)

    # Remove price from top of heap, if it is at the Top, when cancelling
    def update_bbo_when_cancel(self, side, price):
        self.maintain_heap_invariant()
        if side == "bid":
            if -price == self.max_heap[0]:
                pq.heappop(self.max_heap)
            self.price_to_order.pop(price)
        if side == "ask":
            if price == self.min_heap[0]:
                pq.heappop(self.min_heap)
            self.price_to_order.pop(price)

    def update_bbo_when_market(self, side, qty):
        self.maintain_heap_invariant()
        if side == 'bid':

            # If desired quantity = 0 or order book is empty, end function
            if self.order_book[side] == {} or qty == 0:
                return qty, 0

            curr_qty = self.order_book[side][self.price_to_order[-self.max_heap[0]]]['quantity']

            # If desired quantity is larger than quantity in the best order
            if qty >= curr_qty:
                price = pq.heappop(self.max_heap)
                order_id = self.price_to_order.pop(price)
                self.order_book[side].pop(order_id)
                self.fulfilled.add(order_id)
                next = self.update_bbo_when_market(side, qty - curr_qty)
                return next[0], price * curr_qty + next[1]

            else:
                price = self.max_heap[0]
                order_id = self.price_to_order[price]
                self.order_book[side][order_id]['quantity'] -= qty
                return 0, price * qty
        if side == 'ask':

            if self.order_book[side] == {} or qty == 0:
                return qty, 0

            curr_qty = self.order_book[side][self.price_to_order[self.min_heap[0]]]['quantity']

            if qty >= curr_qty:
                price = pq.heappop(self.min_heap)
                order_id = self.price_to_order.pop(price)
                self.order_book[side].pop(order_id)
                self.fulfilled.add(order_id)
                next = self.update_bbo_when_market(side, qty - curr_qty)
                return next[0], price * curr_qty + next[1]

            else:
                price = self.min_heap[0]
                order_id = self.price_to_order[price]
                self.order_book[side][order_id]['quantity'] -= qty
                return 0, price * qty

    def bbo(self):
        self.maintain_heap_invariant()
        print([self.max_heap[0], self.min_heap[0]])


if __name__ == '__main__':
    lob_example = order_book()
    lob_example.add_limit_order('ask', 'Shakti', 10, 1000)
    lob_example.add_limit_order('ask', 'Nikhil', 5, 130)
    lob_example.add_limit_order('bid', 'Atib', 30, 105)
    lob_example.add_limit_order('bid', 'Sanskar', 20, 180)
    print(lob_example.order_book)
    lob_example.add_limit_order('ask', 'Manjit', 10, 95)
    print(lob_example.place_market_order('ask', 12))
    print(lob_example.order_book)
    print(lob_example.place_market_order('ask', 90))
    print(lob_example.order_book)
    lob_example.cancel_limit_order(2)
    lob_example.cancel_limit_order(26)
