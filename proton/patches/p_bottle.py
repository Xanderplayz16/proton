def __patch__():
    from proton.patches import bottle_fake as btl_fake
    import bottle as btl_real
    btl_real = btl_fake
