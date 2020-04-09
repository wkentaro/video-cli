def get_macro_block_size(size):
    for macro_block_size in range(16, 0, -1):
        if size[0] % macro_block_size == 0 and size[1] % macro_block_size == 0:
            break
    return macro_block_size
