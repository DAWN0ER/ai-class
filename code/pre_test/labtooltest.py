from domain.character import (
    Student,
    broadcast,
)
import domain.labtools as lab

Student("林子涵", 0.1, 50)
Student("徐欣怡", 0.1, 50)

broadcast("[校长][徐清远]自我介绍一下。")
lab.create_json_script()
