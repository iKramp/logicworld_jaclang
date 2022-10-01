/// expect 55

/// fibonacci

func fib(n) {
    if n < 2
        return n
    return fib(n - 1) + fib(n - 2)
}

func main() {
    return fib(10)
}