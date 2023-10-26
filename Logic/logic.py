import random
import os
import pandas as pd
import copy
from docx import Document
from docx.shared import Cm,Inches,Twips
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.text import WD_BREAK
import docx2pdf
from PyPDF2 import PdfMerger

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Spacer,Paragraph,Image
from reportlab.lib import colors
from reportlab.lib.units import inch,cm
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle

# Left shift function to cause no problem
def superlogic(date,exam,rooms,tot,single,girls,mselected_faculty,fselected_faculty):
    day_list = []
    print(girls)

    def leftshift(invigilators):
        shift=3
        for a in range(shift):
            temp=invigilators[0]
            b=0
            for b1 in range(len(invigilators)-1):
                invigilators[b1]=invigilators[b1+1]
                b=b1
            invigilators[b]=temp
        return invigilators

    # Required exam dates here

    dates=date

    # Start of Main function

    def generateResult(roomsPerDay,girls):
        staffIndex = 0
        dates_number = 0
        girl = 0

        #Initializing the count for each staff
        '''
        designation_count = {i:0 for i in invigilators}
        '''

        for j in range(len(roomsPerDay)):

            temp_alls = []
            
            start_ind = 0
            
            session = 'FN' #if j == 0 else 'AN' # set session to FN for first day (internal assessment), AN for other days (model exams)
            print('after2')
            global girlss
            print(date,rooms,single,girls,mselected_faculty,fselected_faculty)
            print('af')
            singles = single 
            girls_rooms={}
            '''Boys rooms dictionary'''
            for i in girls:
                girls_rooms[i]=[]
            girls=set(girls)
            allr=set(rooms)
            byr=allr-girls
            boys_rooms={}
            for i in byr:
                boys_rooms[i]=[]
            print(all_rooms,boys_rooms,girls_rooms,invigilators,b_invi,g_invi)
            all_roomsAlloc = copy.deepcopy(rooms)
            boys_roomAllocation = copy.deepcopy(boys_rooms)
            girls_roomAllocation = copy.deepcopy(girls_rooms)


            #to check the count of staff 'x' designation

            '''            
            while(designation_count[invigilators[staffIndex]] == designation[invigilators[staffIndex]] and staffIndex != totalTeachers):
                staffIndex++
            '''

            if staffIndex == len(b_invi):
                leftshift(invigilators)
                staffIndex = 0

            for room in all_roomsAlloc:
                
                if room in girls_roomAllocation and room not in singles and g_invi[girl] not in temp_alls:
                    girls_roomAllocation[room].append(g_invi[girl])
                    temp_alls.append(g_invi[girl])
                    updateStaff(g_invi[girl])
                    work[g_invi[girl]][dates[dates_number]]=room
                    girl += 1
                    if girl == len(g_invi):
                        leftshift(g_invi)
                        girl = 0

                elif room in singles:

                    if room in boys_roomAllocation:
                        if b_invi[staffIndex] not in temp_alls:
                            boys_roomAllocation[room].append(b_invi[staffIndex])
                            updateStaff(b_invi[staffIndex])
                            temp_alls.append(b_invi[staffIndex])
                            work[b_invi[staffIndex]][dates[dates_number]]=room
                            staffIndex += 1
                            if staffIndex == len(b_invi):
                                leftshift(b_invi)
                                staffIndex = 0
                        else:
                            boys_roomAllocation[room].append(g_invi[girl])
                            temp_alls.append(g_invi[girl])
                            updateStaff(g_invi[girl])
                            work[g_invi[girl]][dates[dates_number]]=room
                            girl += 1
                            if girl == len(g_invi):
                                leftshift(g_invi)
                                girl = 0

                    
                    elif room in girls_roomAllocation:
                        girls_roomAllocation[room].append(g_invi[girl])
                        temp_alls.append(g_invi[girl])
                        updateStaff(g_invi[girl])
                        work[g_invi[girl]][dates[dates_number]]=room
                        girl += 1
                        if girl == len(g_invi):
                            leftshift(g_invi)
                            girl = 0
                    
                elif room in boys_roomAllocation:
                    if b_invi[staffIndex] not in temp_alls:
                        boys_roomAllocation[room].append(b_invi[staffIndex])
                        temp_alls.append(b_invi[staffIndex])
                        updateStaff(b_invi[staffIndex])
                        work[b_invi[staffIndex]][dates[dates_number]]=room
                        staffIndex += 1
                        if staffIndex == len(b_invi):
                            leftshift(b_invi)
                            staffIndex = 0
                    else:
                        boys_roomAllocation[room].append(g_invi[girl])
                        temp_alls.append(g_invi[girl])
                        updateStaff(g_invi[girl])
                        work[g_invi[girl]][dates[dates_number]]=room
                        girl += 1
                        if girl == len(g_invi):
                            leftshift(g_invi)
                            girl = 0


            for room in all_roomsAlloc:
                
                if room in girls_roomAllocation and room not in singles and g_invi[girl] not in temp_alls:
                    girls_roomAllocation[room].append(g_invi[girl])
                    temp_alls.append(g_invi[girl])
                    updateStaff(g_invi[girl])
                    work[g_invi[girl]][dates[dates_number]]=room
                    girl += 1
                    if girl == len(g_invi):
                        leftshift(g_invi)
                        girl = 0

                elif room in singles:
                    continue
                    
                elif room in boys_roomAllocation:
                    if b_invi[staffIndex] not in temp_alls:
                        boys_roomAllocation[room].append(b_invi[staffIndex])
                        temp_alls.append(b_invi[staffIndex])
                        updateStaff(b_invi[staffIndex])
                        work[b_invi[staffIndex]][dates[dates_number]]=room
                        staffIndex += 1
                        if staffIndex == len(b_invi):
                            leftshift(b_invi)
                            staffIndex = 0
                    else:
                        boys_roomAllocation[room].append(g_invi[girl])
                        temp_alls.append(g_invi[girl])
                        updateStaff(g_invi[girl])
                        work[g_invi[girl]][dates[dates_number]]=room
                        girl += 1
                        if girl == len(g_invi):
                            leftshift(g_invi)
                            girl = 0
            
                '''

                Code for if only one floor (test)

                if(gender[invigilators[staffIndex]] == 'F' and k<len(girls_rooms)):
                    girls_roomAllocation[f'S{k+1}'].append(invigilators[staffIndex])
                    updateStaff(invigilators[staffIndex])
                    #To add each assigned classroom to staffs
                    work[invigilators[staffIndex]][dates[dates_number]]=f'S{k+1}'
                    staffIndex += 1
                    if(len(girls_roomAllocation[f'S{k+1}'])==2):
                        k+=1
                
                else:
                    if(f"S{l+1}" in not_needed):
                        l+=1
                        continue
                        
                    boys_roomAllocation[f'S{l+1}'].append(invigilators[staffIndex])
                    #To add each assigned classroom to staffs
                    work[invigilators[staffIndex]][dates[dates_number]]=f'S{l+1}'

                    updateStaff(invigilators[staffIndex])
                    staffIndex += 1
                    if(f"S{l+1}" == "S24"):
                        l+=1
                    elif(f"S{l+1}"=="S26"):
                        break
                    else:
                        if(len(boys_roomAllocation[f'S{l+1}'])==2):
                            l+=1

                '''
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Spacer
            from reportlab.lib import colors
            from reportlab.lib.units import inch,cm
            from reportlab.lib.styles import getSampleStyleSheet

            doc = SimpleDocTemplate(f"Day_{j+1}_Room_Allocation.pdf", pagesize=letter)

            elements = []

            header_data = [
                [f"{exam}\n"],
                [f"Exam duty list                                    Date={dates[dates_number]}\n"],
            ]
            header_table = Table(header_data, colWidths=6.9*inch, rowHeights=1.3 * cm)
            header_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (0, 1), (-1, 1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 0.3 * cm),
                ('BACKGROUND', (0, 1), (-1, 1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 0), (-1, -1), 15),
            ]))
            data = [
                ["Hall","Faculty","Time","Signature"]
            ]
            key=list(girls_roomAllocation.keys())
            key2=list(boys_roomAllocation.keys())
            key=key+key2
            key.sort()
            print(key)
            totaldict=girls_roomAllocation.copy()
            totaldict.update(boys_roomAllocation)
            for keyg in totaldict:
                if len(totaldict[keyg]) == 1:
                    data.append([f"{keyg}",f"{totaldict[keyg][0]}",'',''])
                if len(totaldict[keyg]) == 2:
                    data.append([f"{keyg}",f"{totaldict[keyg][0]}\n\n{totaldict[keyg][1]}",'',''])
            # for keyg,itemg in girls_roomAllocation.items():
            #     if len(itemg) == 1:
            #         data.append([f"{keyg}",f"{itemg[0]}",'',''])
            #     if len(itemg) == 2:
            #         data.append([f"{keyg}",f"{itemg[0]}\n\n{itemg[1]}",'',''])
            # for keyb,itemb in boys_roomAllocation.items():
            #     if len(itemb) == 1:
            #         data.append([f"{keyb}",f"{itemb[0]}",'',''])
            #     if len(itemb) == 2:
            #         data.append([f"{keyb}",f"{itemb[0]}\n\n{itemb[1]}",'',''])
            
            style = TableStyle([
                # ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                # ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
            ])
            # print(data)
            table = Table(data,colWidths=[0.8*inch,3*inch,1.4*inch,1.7*inch],rowHeights=0.6*inch)
            table.setStyle(style)

            # Add the table to the list of elements
            elements.append(header_table) 
            elements.append(table)
            
            # Build the PDF document
            doc.build(elements)

            day_list.append(f"Day_{j+1}_Room_Allocation.pdf")

            dates_number += 1
        

        # Out of the loop

        '''Merger'''

        merger = PdfMerger()
        for pdf in day_list:
            merger.append(pdf)
        merger.write("merged_days.pdf")

        '''Work Schedule'''

        doc = SimpleDocTemplate(f"Invigilator_Work_Schedule.pdf", pagesize=letter)

        elements = []

        header_data = [
                ["Office of the Controller of Examination\n"],
                [f"{exam} 2023-DUTY LIST\n"],
            ]
        header_table = Table(header_data, colWidths=6.9*inch, rowHeights=1.3 * cm)
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 1), (-1, 1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 0.3 * cm),
            ('BACKGROUND', (0, 1), (-1, 1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 15),
        ]))


        data = [
            ["Staff Name"]
        ]
        datapos=1
        for jk in dates:
            data[0].append(jk)
        for name,dutylist in work.items():
            data.append([f"{name}"])
            for dayets,rum in dutylist.items():
                data[datapos].append(rum)
            datapos += 1
        
        
        style = TableStyle([
            # ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            # ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
        ])
        table = Table(data,rowHeights=0.6*inch)
        table.setStyle(style)

        # Add the table to the list of elements
        elements.append(header_table) 
        elements.append(Spacer(1, 0.1 * letter[1]))
        elements.append(table)
        
        # Build the PDF document
        doc.build(elements)



        '''Work Count'''

        doc = SimpleDocTemplate(f"Invigilator_Work_Count.pdf", pagesize=letter)

        elements = []

        header_data = [
                ["Office of the Controller of Examination\n"],
                [f"{exam} 2023-DUTY Count\n"],
            ]
        header_table = Table(header_data, colWidths=6.9*inch, rowHeights=1.3 * cm)
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 1), (-1, 1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 0.3 * cm),
            ('BACKGROUND', (0, 1), (-1, 1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 15),
        ]))

        data =[
            ["Name","Count"]
        ]

        for keys,value in Invigilator_work_count.items():
            data.append([f"{keys}",f"{value}"])

        style = TableStyle([
            # ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            # ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
        ])
        # print(data)
        table = Table(data,colWidths=[3.6*inch,3.3*inch],rowHeights=0.6*inch)
        table.setStyle(style)

        # Add the table to the list of elements
        elements.append(header_table) 
        elements.append(table)
        
        # Build the PDF document
        doc.build(elements)



    def updateStaff(staff):
        Invigilator_work_count[staff] += 1


    # Required Datas 
    dataset = pd.read_csv('Newstaffs.csv', encoding= 'unicode_escape')

    invigilators = mselected_faculty+fselected_faculty

    b_invi = mselected_faculty
    g_invi = fselected_faculty

    random.shuffle(b_invi)
    random.shuffle(g_invi)


    #to get the gender


    #Boys and Girls Input List
    '''
    First__rooms_available=[f'F{i}' for i in range(27)]
    girl_needed_rooms=[]
    boy_needed_rooms=[]
    '''

    '''All Needed rooms'''

    all_rooms = rooms
    '''Singles staff rooms'''

    singles = single 
    girls_rooms={}
    '''Boys rooms dictionary'''
    for i in girls:
        girls_rooms[i]=[]
    gir=set(girls)
    allr=set(rooms)
    byr=allr-gir
    boys_rooms={}
    for i in byr:
        boys_rooms[i]=[]
    Invigilator_work_count = {i:0 for i in invigilators}



    work={i:{j:"-" for j in dates} for i in invigilators}

    # Shuffle Staffs
    random.shuffle(invigilators)

    # Rooms needed each day (can be extended)
    roomsPerDay = [len(rooms) for i in range(tot)]   

    generateResult(roomsPerDay,girls)

# for pdf in day_list:
#      os.remove(pdf)
def endsem(name,single_date,sessions,exam1,depttar): # do for single day each time
        faculty1 = name
        print("Faculty = ",faculty1)
        faculty={}
        for i in range(len(name)):
            k=name[i]
            faculty[k]={}
            faculty[k]["duty"]=exam1[i]
            faculty[k]['session']=sessions[i]
        print('\n\nfac',faculty)
        print(faculty1)
        random.shuffle(faculty1)

        # <------------- FOR Internal------------>

        doc = SimpleDocTemplate(f"Internal_Allocation.pdf", pagesize=letter)
        elements = []
        # tempdate = dates[dates_number].split('-')[::-1]
        header_data = [
            [f"Office of Controller of Examination"],
            [f"End Semester Examination - 2023"],
            [f"DUTY LIST {single_date}"],
            [f"Reporting room : MT6"],
        ]
        header_table = Table(header_data, colWidths=7.4*inch, rowHeights=2 * cm)
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 0.3 * cm),
            ('BACKGROUND', (0, 1), (-1, 1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 15),
        ]))

        sno = 1
        data = [
            ["S.no","Name of the Faculty","Department","Session","Duty Venue"]
        ]

        for name in faculty1:
            if faculty[name]['duty'] == "external":
                pass
            else:
                sess = faculty[name]['session'].upper()
                data.append([f"{sno}",f"{name}",f"{depttar[name]}",f"{sess}","CIT"])
                sno += 1

        style = TableStyle([
            # ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            # ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
        ])
        # print(data)
        table = Table(data,colWidths=[0.5*inch,3.3*inch,1.4*inch,1.1*inch,1.1*inch],rowHeights=0.6*inch)
        table.setStyle(style)
        signature_data = [["Signature of COE", "Signature of Principal"],
        ]
        signature_table = Table(signature_data, colWidths=[3.7*inch, 3.7*inch], rowHeights=2*inch)
        signature_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.1, colors.white),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
        ]))

        # from django.templatetags.static import static

        # full_path = static('images/cit.png')

        # header_img = Image(full_path, 50, 150)

        # Add the table to the list of elements

        # elements.append(header_img)
        elements.append(header_table) 
        elements.append(table)
        elements.append(signature_table)

        '''To Append the final paragraphs'''


        sstyle = getSampleStyleSheet()
        yourStyle = ParagraphStyle('yourtitle',
        fontName="Helvetica",
        fontSize=16,
        parent=sstyle['Heading2'],
        alignment=2,
        spaceBefore=1*inch,
        spaceAfter=4
        )
        headStyle = ParagraphStyle('headtitle',
        fontName="Helvetica-Bold",
        fontSize=18,
        parent=sstyle['Heading1'],
        alignment=0,
        spaceBefore=3*inch,
        spaceAfter=0.4*inch
        )
        paraStyle = ParagraphStyle('paratitle',
        fontName="Helvetica",
        fontSize=15,
        parent=sstyle['Heading2'],
        alignment=0,
        spaceAfter=0.4*inch
        )
        tailStyle = ParagraphStyle('tailtitle',
        fontName="Helvetica-Bold",
        fontSize=20,
        parent=sstyle['Heading1'],
        alignment=0,
        spaceBefore=0.5*inch,
        )
        # text_content1 = '''Signature of Principal'''
        # text_content2 = '''Signature of COE/DCOE'''
        Head = 'Follow the below instructions , any deviation will be viewed seriously' 
        body = '''
        1. Collect the Question paper and Answer sheets on or before 30 mins<br /><br />
        2. Mobile phones are not allowed inside the hall<br /><br />
        3. Strictly monitor the students, it is not advisable to sit inside the exam hall.<br /><br />
        4. All have to collect the answer sheet in registration order in their respective
        halls at the end of the examination and submit the same to the COE office<br /><br />
        5. Any alteration of duty should be done with the knowledge of COE/DCOE
        '''
        tail = 'Kind Note: This allocation is generated by system, suggestion and feedback is welcomed'

        # P = Paragraph(text_content1, yourStyle)
        # Pz = Paragraph(text_content2, yourStyle)
        P1 = Paragraph(Head, headStyle)
        P2 = Paragraph(body, paraStyle)
        P3 = Paragraph(tail, tailStyle)
        # elements.append(P)
        # elements.append(Pz)
        elements.append(P1)
        elements.append(P2)
        elements.append(P3)
        
        # Build the PDF document
        doc.build(elements)


        # <------------- FOR External------------>


        doc = SimpleDocTemplate(f"External_Allocation.pdf", pagesize=letter)
        elements = []
        # tempdate = dates[dates_number].split('-')[::-1]
        header_data = [
            [f"Office of Controller of  Examination"],
            [f"End Semester Examination - 2023"],
            [f"DUTY LIST {single_date}"],
        ]
        header_table = Table(header_data, colWidths=7.4*inch, rowHeights=2 * cm)
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 0.3 * cm),
            ('BACKGROUND', (0, 1), (-1, 1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 15),
        ]))

        sno = 1

        data = [
            ["S.no","Name of the Faculty","Department","Session","Duty Venue"]
        ]

        for name in faculty1:
            if faculty[name]['duty'] == "internal":
                pass
            else:
                sess = faculty[name]['session'].upper()
                data.append([f"{sno}",f"{name}",f"{depttar[name]}",f"{sess}","PEC"])
                sno += 1

        style = TableStyle([
            # ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            # ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
        ])
        # print(data)
        table = Table(data,colWidths=[0.5*inch,3.3*inch,1.4*inch,1.1*inch,1.1*inch],rowHeights=0.6*inch)
        table.setStyle(style)
        signature_data = [["Signature of COE", "Signature of Principal"],
        ]
        signature_table = Table(signature_data, colWidths=[3.7*inch, 3.7*inch], rowHeights=2*inch)
        signature_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.1, colors.white),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
        ]))

        # Add the table to the list of elements
        # elements.append(header_img)
        elements.append(header_table) 
        elements.append(table)
        elements.append(P)        
        elements.append(Pz)
        elements.append(signature_table)


        # Build the PDF document
        doc.build(elements)
