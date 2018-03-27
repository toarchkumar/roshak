import canvas.crm3558.cron as crm3558

def app():
    crm3558.update_from_s3()
    crm3558.inkbolt_m1()
    crm3558.inkbolt_m2()
    crm3558.inkbolt_m3()
    crm3558.inkbolt_m4()
    crm3558.inkbolt_m5()

if __name__ == '__main__':
    app()