#!/bin/bash
pip install -r requirements.txt
prisma py fetch
prisma generate
