#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from project import app
from logging import FileHandler, WARNING

file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)
app.logger.addHandler(file_handler)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run('0.0.0.0', port=port)
