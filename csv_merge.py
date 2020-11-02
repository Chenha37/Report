import pandas as pd
import csv
import sklearn
from sklearn import metrics
from shutil import copyfile

if __name__ == '__main__':


    # make a copy to the DB and make a new DB with the relevant colloumns
    copyfile('DB.csv', 'CopyDB.csv')
    file = pd.read_csv('CopyDB.csv', usecols=['title', 'movie_id', 'cast', 'crew', 'budget', 'revenue'], low_memory=False)
    file.to_csv('NewDB.csv')

    
    # make only the crew list
    file = pd.read_csv('NewDB.csv', usecols=['crew'], low_memory=False)
    file.to_csv('Crew.csv')
   
    # make the directors info
    data = ['Name','Job', 'ID']
    out = csv.writer(open('Directors.csv', "w", newline=''), delimiter=',', quoting=csv.QUOTE_ALL)
    out.writerow(data)
    for row in file.iterrows():
        array = row[1].str.split(',')
        size = len(array[0])/6
        for counter in range(int(size)):
            job = [array[0][4 + 6 * counter]]
            name = [array[0][4 + 6 * counter+1]]
            id = [array[0][4 + 6 * counter-1]]
            check = " \"job\": \"Director\"" in job[0]
            if check:
                new = name[0].split(':')
                new1 = new[1].split('}')
                out.writerow([name[0].split(':')[1].split('}')[0], job[0].split(':')[1], id[0].split(':')[1]])


    # make the producers info
    data = ['Name', 'Job', 'ID']
    out = csv.writer(open('Producers.csv', "w", newline=''), delimiter=',', quoting=csv.QUOTE_ALL)
    out.writerow(data)
    for row in file.iterrows():
        array = row[1].str.split(',')
        size = len(array[0]) / 6
        for counter in range(int(size)):
            job = [array[0][4 + 6 * counter]]
            name = [array[0][4 + 6 * counter + 1]]
            id = [array[0][4 + 6 * counter - 1]]
            check = " \"job\": \"Producer\"" in job[0]
            if check:
                new = name[0].split(":")
                new1 = new[1].split('}')
                out.writerow([name[0].split(':')[1].split('}')[0], job[0].split(':')[1], id[0].split(':')[1]])
    
    # make the writers info
    data = ['Name', 'Job', 'ID']
    out = csv.writer(open('Writers.csv', "w", newline=''), delimiter=',', quoting=csv.QUOTE_ALL)
    out.writerow(data)
    for row in file.iterrows():
        array = row[1].str.split(',')
        size = len(array[0]) / 6
        for counter in range(int(size)):
            job = [array[0][4 + 6 * counter]]
            name = [array[0][4 + 6 * counter + 1]]
            id = [array[0][4 + 6 * counter - 1]]
            check = " \"job\": \"Writer\"" in job[0] or " \"job\": \"Story\"" in job[0] or " \"job\": \"Author\"" in job[0] or " \"job\": \"Screenplay\"" in job[0] or " \"job\": \"Screenstory\"" in job[0]
            if check:
                new = name[0].split(":")
                new1 = new[1].split('}')
                out.writerow([name[0].split(':')[1].split('}')[0], job[0].split(':')[1], id[0].split(':')[1]])


    # make new file without duplicated writers
    dictionary = {}
    file = pd.read_csv('Writers.csv', low_memory=False)
    data = ["Name", "Job", "ID"]
    out = csv.writer(open('MergedWritersFile.csv', "w", newline=''), delimiter=',', quoting=csv.QUOTE_ALL)
    out.writerow(data)
    for row in file.iterrows():
        if row[1][2] in dictionary:  # id is already exists
            continue
        else:
            dictionary[row[1][2]] = {}
            # new_data = row
            # print(row[1])
            out.writerow(row[1])

    
    
    # make new file without duplicated Producers
    dictionary = {}
    file = pd.read_csv('Producers.csv', low_memory=False)
    data = ["Name", "Job", "ID"]
    out = csv.writer(open('MergedProducersFile.csv', "w", newline=''), delimiter=',', quoting=csv.QUOTE_ALL)
    out.writerow(data)
    for row in file.iterrows():
        if row[1][2] in dictionary:  # id is already exists
            continue
        else:
            dictionary[row[1][2]] = {}
            # new_data = row
            # print(row[1])
            out.writerow(row[1])

    
    
    # make new file without duplicated Directors
    dictionary = {}
    file = pd.read_csv('Directors.csv', low_memory=False)
    data = ["Name", "Job", "ID"]
    out = csv.writer(open('MergedDirectorsFile.csv', "w", newline=''), delimiter=',', quoting=csv.QUOTE_ALL)
    out.writerow(data)
    for row in file.iterrows():
        if row[1][2] in dictionary:  # id is already exists
            continue
        else:
            dictionary[row[1][2]] = {}
            # new_data = row
            # print(row[1])
            out.writerow(row[1])
    file = pd.read_csv('NewDB.csv', usecols=['title', 'movie_id', 'cast', 'crew', 'budget', 'revenue'], low_memory=False)
    file.to_csv('NormalizeFile.csv')
 
 
 
    # normalize the budget and revenue
    file = pd.read_csv('DB.csv', usecols=['movie_id', 'budget', 'revenue'], low_memory=False)
    data = ["movie_id", "budget", "revenue"]
    out = csv.writer(open("Normalize.csv", "w", newline=''), delimiter=',', quoting=csv.QUOTE_ALL)
    out.writerow(data)
    for row in file.iterrows():
        new_data = [row[1][0], row[1][1] / 100000000, (row[1][2]) / 100000000]
        out.writerow(new_data)
    copyfile('normalize.csv', 'normalizeDB.csv')  
  
########################################################################################################################




    ############################################ DB - average for all ##################################################
    
    # calculate the Actor value
    out = csv.writer(open('ActorsGrades.csv', "w", newline=''), delimiter=',', quoting=csv.QUOTE_ALL)
    data = ['ID', 'Name', 'Grade']
    out.writerow(data)
    Actors = pd.read_csv('MergedActorsFile.csv', low_memory=False)
    Normalize = pd.read_csv('Normalize.csv', usecols=['movie_id', 'budget', 'revenue'], low_memory=False)
    Movies = pd.read_csv('NewDB.csv', low_memory=False)
    tal = 0
    for row1 in Actors.iterrows():
         num_movies = 0
         grade = 0
         actor_name = row1[1][2]
         actor_id = "\"id\": "+str(row1[1][1])
         counter = 0
         for row2 in Movies.iterrows():
             counter += 1
             if counter == 61 or counter == 1737 or counter == 2078 or counter == 2348 or counter == 2608 or counter == 2779 or counter == 2791:
                 continue
             if counter == 3142 or counter == 3230 or counter == 3292 or counter == 3398 or counter == 3477 or counter == 3679 or counter == 3776:
                 continue
             if counter == 3905 or counter == 4000 or counter == 4017 or counter == 4076 or counter == 4113 or counter == 4126 or counter == 4148:
                 continue
             if counter == 4185 or counter == 4255 or counter == 4312 or counter == 4321 or counter == 4329 or counter == 4335 or counter == 4394:
                 continue
             if counter == 4408 or counter == 4438 or counter == 4465 or counter == 4475 or counter == 4478 or counter == 4498 or counter == 4510:
                 continue
             if counter == 4511 or counter == 4515 or counter == 4524 or counter == 4533 or counter == 4547 or counter == 4557 or counter == 4560:
                 continue
             if counter == 4569 or counter == 4571 or counter == 4573 or counter == 4578 or counter == 4581 or counter == 4588 or counter == 4590:
                 continue
             if counter == 4596 or counter == 4604 or counter == 4613 or counter == 4623 or counter == 4624 or counter == 4640 or counter == 4645:
                 continue
             if counter == 4664 or counter == 4665 or counter == 4681 or counter == 4686 or counter == 4692 or counter == 4696 or counter == 4705:
                 continue
             if counter == 4717 or counter == 4719 or counter == 4723 or counter == 4726 or counter == 4744 or counter == 4762 or counter == 4764:
                 continue
             if counter == 4786 or counter == 4789 or counter == 4804:
                 continue
             movie_id = row2[1][2]
             actors = row2[1][3].split("{")
             threeMainActors = actors[1] + actors[2] + actors[3]
             check = actor_id in threeMainActors
             if check:
                 for row3 in Normalize.iterrows():
                     if movie_id == row3[1][0]:
                         grade += row3[1][2]
                         num_movies += 1
                         break
         if num_movies != 0:
            grade = grade/num_movies
         new_data = [str(row1[1][1]), actor_name, grade]
         out.writerow(new_data)
         tal += 1
         print(tal)
    
    # calculate the Writer value
    out = csv.writer(open('WritersGrades.csv', "w", newline=''), delimiter=',', quoting=csv.QUOTE_ALL)
    data = ['ID', 'Name', 'Grade']
    out.writerow(data)
    Writers = pd.read_csv('MergedWritersFile.csv', low_memory=False)
    Normalize = pd.read_csv('Normalize.csv',usecols=['movie_id', 'budget', 'revenue'], low_memory=False)
    Movies = pd.read_csv('NewDB.csv', low_memory=False)
    counter = 0
    for row1 in Writers.iterrows():
        num_movies = 0
        grade = 0
        writer_name = row1[1][0]
        writer_id = "\"id\": "+str(row1[1][2])+", "
        for row2 in Movies.iterrows():
            movie_id = row2[1][2]
            crew = row2[1][4]
            check = writer_id + "\"job\": \"Writer\"," in crew or writer_id + "\"job\": \"Story\"," in crew or writer_id + "\"job\": \"Author\"," in crew or writer_id + "\"job\": \"Screenplay\"," in crew or writer_id + "\"job\": \"Screenstory\"," in crew
            if check:
                for row3 in Normalize.iterrows():
                    if movie_id == row3[1][0]:
                        grade += row3[1][2]
                        num_movies += 1
                        break
        if num_movies != 0:
            grade = grade/num_movies
        new_data = [str(row1[1][2]), writer_name, grade]
        out.writerow(new_data)
        counter += 1
        print(counter)

      

    # calculate the Producer value
    out = csv.writer(open('ProducersGrades.csv', "w", newline=''), delimiter=',', quoting=csv.QUOTE_ALL)
    data = ['ID', 'Name', 'Grade']
    out.writerow(data)
    Producers = pd.read_csv('MergedProducersFile.csv', low_memory=False)
    Normalize = pd.read_csv('Normalize.csv',usecols=['movie_id', 'budget', 'revenue'], low_memory=False)
    Movies = pd.read_csv('NewDB.csv', low_memory=False)
    counter = 0
    for row1 in Producers.iterrows():
        num_movies = 0
        grade = 0
        producer_name = row1[1][0]
        producer_id = "\"id\": " + str(row1[1][2]) + ", "
        for row2 in Movies.iterrows():
            movie_id = row2[1][2]
            crew = row2[1][4]
            check = producer_id + "\"job\": \"Producer\"," in crew
            if check:
                for row3 in Normalize.iterrows():
                    if movie_id == row3[1][0]:
                        grade += row3[1][2]
                        num_movies += 1
                        break
        if num_movies != 0:
            grade = grade / num_movies
        new_data = [str(row1[1][2]), producer_name, grade]
        out.writerow(new_data)
        counter += 1
        print(counter)



    # calculate the Director value
    out = csv.writer(open('DirectorsGrades.csv', "w", newline=''), delimiter=',', quoting=csv.QUOTE_ALL)
    data = ['ID', 'Name', 'Grade']
    out.writerow(data)
    Directors = pd.read_csv('MergedDirectorsFile.csv', low_memory=False)
    Normalize = pd.read_csv('Normalize.csv', usecols=['movie_id', 'budget', 'revenue'], low_memory=False)
    Movies = pd.read_csv('NewDB.csv', low_memory=False)
    counter = 0
    for row1 in Directors.iterrows():
        num_movies = 0
        grade = 0
        director_name = row1[1][0]
        director_id = "\"id\": " + str(row1[1][2]) + ", "
        for row2 in Movies.iterrows():
            movie_id = row2[1][2]
            crew = row2[1][4]
            check = director_id + "\"job\": \"Director\"," in crew
            if check:
                for row3 in Normalize.iterrows():
                    if movie_id == row3[1][0]:
                        grade += row3[1][2]
                        num_movies += 1
                        break
        if num_movies != 0:
            grade = grade / num_movies
        new_data = [str(row1[1][2]), director_name, grade]
        out.writerow(new_data)
        counter += 1
        print(counter)
 

    # make the DBclassification for average for all
    DB = pd.read_csv('NewDB.csv', usecols=['title', 'movie_id', 'cast', 'crew'], low_memory=False)
    Normalized = pd.read_csv('Normalize.csv', usecols=['movie_id', 'budget', 'revenue'], low_memory=False)
    inDB = csv.writer(open('DBclassified.csv', "w", newline=''), delimiter=',', quoting=csv.QUOTE_ALL)
    inDB = pd.merge(DB, Normalized, on='movie_id')
    inDB.to_csv('DBclassified.csv')

    ############################################ DB - Max for 3 jobs and actor average #################################
    # calculate the Actor value
    out = csv.writer(open('ActorsGrades.csv', "w", newline=''), delimiter=',', quoting=csv.QUOTE_ALL)
    data = ['ID', 'Name', 'Grade']
    out.writerow(data)
    Actors = pd.read_csv('MergedActorsFile.csv', low_memory=False)
    Normalize = pd.read_csv('Normalize.csv', usecols=['movie_id', 'budget', 'revenue'], low_memory=False)
    Movies = pd.read_csv('NewDB.csv', low_memory=False)
    tal = 0
    for row1 in Actors.iterrows():
         num_movies = 0
         grade = 0
         actor_name = row1[1][2]
         actor_id = "\"id\": "+str(row1[1][1])
         counter = 0
         for row2 in Movies.iterrows():
             counter += 1
             if counter == 61 or counter == 1737 or counter == 2078 or counter == 2348 or counter == 2608 or counter == 2779 or counter == 2791:
                 continue
             if counter == 3142 or counter == 3230 or counter == 3292 or counter == 3398 or counter == 3477 or counter == 3679 or counter == 3776:
                 continue
             if counter == 3905 or counter == 4000 or counter == 4017 or counter == 4076 or counter == 4113 or counter == 4126 or counter == 4148:
                 continue
             if counter == 4185 or counter == 4255 or counter == 4312 or counter == 4321 or counter == 4329 or counter == 4335 or counter == 4394:
                 continue
             if counter == 4408 or counter == 4438 or counter == 4465 or counter == 4475 or counter == 4478 or counter == 4498 or counter == 4510:
                 continue
             if counter == 4511 or counter == 4515 or counter == 4524 or counter == 4533 or counter == 4547 or counter == 4557 or counter == 4560:
                 continue
             if counter == 4569 or counter == 4571 or counter == 4573 or counter == 4578 or counter == 4581 or counter == 4588 or counter == 4590:
                 continue
             if counter == 4596 or counter == 4604 or counter == 4613 or counter == 4623 or counter == 4624 or counter == 4640 or counter == 4645:
                 continue
             if counter == 4664 or counter == 4665 or counter == 4681 or counter == 4686 or counter == 4692 or counter == 4696 or counter == 4705:
                 continue
             if counter == 4717 or counter == 4719 or counter == 4723 or counter == 4726 or counter == 4744 or counter == 4762 or counter == 4764:
                 continue
             if counter == 4786 or counter == 4789 or counter == 4804:
                 continue
             movie_id = row2[1][2]
             actors = row2[1][3].split("{")
             threeMainActors = actors[1] + actors[2] + actors[3]
             check = actor_id in threeMainActors
             if check:
                 for row3 in Normalize.iterrows():
                     if movie_id == row3[1][0]:
                         grade += row3[1][2]
                         num_movies += 1
                         break
         if num_movies != 0:
            grade = grade/num_movies
         new_data = [str(row1[1][1]), actor_name, grade]
         out.writerow(new_data)
         tal += 1
         print(tal)
         if tal == 3:
            break

    # calculate the Writer value
    out = csv.writer(open('WritersGrades.csv', "w", newline=''), delimiter=',', quoting=csv.QUOTE_ALL)
    data = ['ID', 'Name', 'Grade']
    out.writerow(data)
    Writers = pd.read_csv('MergedWritersFile.csv', low_memory=False)
    Normalize = pd.read_csv('Normalize.csv',usecols=['movie_id', 'budget', 'revenue'], low_memory=False)
    Movies = pd.read_csv('NewDB.csv', low_memory=False)
    counter = 0
    for row1 in Writers.iterrows():
        grade = 0
        writer_name = row1[1][0]
        writer_id = "\"id\": "+str(row1[1][2])+", "
        for row2 in Movies.iterrows():
            movie_id = row2[1][2]
            crew = row2[1][4]
            check = writer_id + "\"job\": \"Writer\"," in crew or writer_id + "\"job\": \"Story\"," in crew or writer_id + "\"job\": \"Author\"," in crew or writer_id + "\"job\": \"Screenplay\"," in crew or writer_id + "\"job\": \"Screenstory\"," in crew
            if check:
                for row3 in Normalize.iterrows():
                    if movie_id == row3[1][0]:
                        if grade < row3[1][2]:
                            grade = row3[1][2]
                        break
        new_data = [str(row1[1][2]), writer_name, grade]
        out.writerow(new_data)
        counter += 1
        print(counter)
        

    # calculate the Producer value
    out = csv.writer(open('ProducersGrades.csv', "w", newline=''), delimiter=',', quoting=csv.QUOTE_ALL)
    data = ['ID', 'Name', 'Grade']
    out.writerow(data)
    Producers = pd.read_csv('MergedProducersFile.csv', low_memory=False)
    Normalize = pd.read_csv('Normalize.csv',usecols=['movie_id', 'budget', 'revenue'], low_memory=False)
    Movies = pd.read_csv('NewDB.csv', low_memory=False)
    counter = 0
    for row1 in Producers.iterrows():
        grade = 0
        producer_name = row1[1][0]
        producer_id = "\"id\": " + str(row1[1][2]) + ", "
        for row2 in Movies.iterrows():
            movie_id = row2[1][2]
            crew = row2[1][4]
            check = producer_id + "\"job\": \"Producer\"," in crew
            if check:
                for row3 in Normalize.iterrows():
                    if movie_id == row3[1][0]:
                        if grade < row3[1][2]:
                            grade = row3[1][2]
                        break
        new_data = [str(row1[1][2]), producer_name, grade]
        out.writerow(new_data)
        counter += 1
        print(counter)

    # calculate the Director value
    out = csv.writer(open('DirectorsGrades.csv', "w", newline=''), delimiter=',', quoting=csv.QUOTE_ALL)
    data = ['ID', 'Name', 'Grade']
    out.writerow(data)
    Directors = pd.read_csv('MergedDirectorsFile.csv', low_memory=False)
    Normalize = pd.read_csv('Normalize.csv', usecols=['movie_id', 'budget', 'revenue'], low_memory=False)
    Movies = pd.read_csv('NewDB.csv', low_memory=False)
    counter = 0
    for row1 in Directors.iterrows():
        grade = 0
        director_name = row1[1][0]
        director_id = "\"id\": " + str(row1[1][2]) + ", "
        for row2 in Movies.iterrows():
            movie_id = row2[1][2]
            crew = row2[1][4]
            check = director_id + "\"job\": \"Director\"," in crew
            if check:
                for row3 in Normalize.iterrows():
                    if movie_id == row3[1][0]:
                        if grade < row3[1][2]:
                            grade = row3[1][2] 
                        break
        new_data = [str(row1[1][2]), director_name, grade]
        out.writerow(new_data)
        counter += 1
        print(counter)
 

    # make the DBclassification for max for 3 jobs and average for actors 
    DB = pd.read_csv('NewDB.csv', usecols=['title', 'movie_id', 'cast', 'crew'], low_memory=False)
    Normalized = pd.read_csv('Normalize.csv', usecols=['movie_id', 'budget', 'revenue'], low_memory=False)
    inDB = csv.writer(open('DBclassified.csv', "w", newline=''), delimiter=',', quoting=csv.QUOTE_ALL)
    inDB = pd.merge(DB, Normalized, on='movie_id')
    inDB.to_csv('DBclassified.csv')

     ############################################ DB - Max for all #####################################################
    # calculate the Actor value
    out = csv.writer(open('ActorsGrades.csv', "w", newline=''), delimiter=',', quoting=csv.QUOTE_ALL)
    data = ['ID', 'Name', 'Grade']
    out.writerow(data)
    Actors = pd.read_csv('MergedActorsFile.csv', low_memory=False)
    Normalize = pd.read_csv('Normalize.csv', usecols=['movie_id', 'budget', 'revenue'], low_memory=False)
    Movies = pd.read_csv('NewDB.csv', low_memory=False)
    tal = 0
    for row1 in Actors.iterrows():
         grade = 0
         actor_name = row1[1][2]
         actor_id = "\"id\": "+str(row1[1][1])
         counter = 0
         for row2 in Movies.iterrows():
             counter += 1
             if counter == 61 or counter == 1737 or counter == 2078 or counter == 2348 or counter == 2608 or counter == 2779 or counter == 2791:
                 continue
             if counter == 3142 or counter == 3230 or counter == 3292 or counter == 3398 or counter == 3477 or counter == 3679 or counter == 3776:
                 continue
             if counter == 3905 or counter == 4000 or counter == 4017 or counter == 4076 or counter == 4113 or counter == 4126 or counter == 4148:
                 continue
             if counter == 4185 or counter == 4255 or counter == 4312 or counter == 4321 or counter == 4329 or counter == 4335 or counter == 4394:
                 continue
             if counter == 4408 or counter == 4438 or counter == 4465 or counter == 4475 or counter == 4478 or counter == 4498 or counter == 4510:
                 continue
             if counter == 4511 or counter == 4515 or counter == 4524 or counter == 4533 or counter == 4547 or counter == 4557 or counter == 4560:
                 continue
             if counter == 4569 or counter == 4571 or counter == 4573 or counter == 4578 or counter == 4581 or counter == 4588 or counter == 4590:
                 continue
             if counter == 4596 or counter == 4604 or counter == 4613 or counter == 4623 or counter == 4624 or counter == 4640 or counter == 4645:
                 continue
             if counter == 4664 or counter == 4665 or counter == 4681 or counter == 4686 or counter == 4692 or counter == 4696 or counter == 4705:
                 continue
             if counter == 4717 or counter == 4719 or counter == 4723 or counter == 4726 or counter == 4744 or counter == 4762 or counter == 4764:
                 continue
             if counter == 4786 or counter == 4789 or counter == 4804:
                 continue
             movie_id = row2[1][2]
             actors = row2[1][3].split("{")
             threeMainActors = actors[1] + actors[2] + actors[3]
             check = actor_id in threeMainActors
             if check:
                 for row3 in Normalize.iterrows():
                     if movie_id == row3[1][0]:
                         if grade < row3[1][2]:
                            grade = row3[1][2] 
                         break
         new_data = [str(row1[1][1]), actor_name, grade]
         out.writerow(new_data)
         tal += 1
         print(tal)


    # calculate the Writer value
    out = csv.writer(open('WritersGrades.csv', "w", newline=''), delimiter=',', quoting=csv.QUOTE_ALL)
    data = ['ID', 'Name', 'Grade']
    out.writerow(data)
    Writers = pd.read_csv('MergedWritersFile.csv', low_memory=False)
    Normalize = pd.read_csv('Normalize.csv',usecols=['movie_id', 'budget', 'revenue'], low_memory=False)
    Movies = pd.read_csv('NewDB.csv', low_memory=False)
    counter = 0
    for row1 in Writers.iterrows():
        grade = 0
        writer_name = row1[1][0]
        writer_id = "\"id\": "+str(row1[1][2])+", "
        for row2 in Movies.iterrows():
            movie_id = row2[1][2]
            crew = row2[1][4]
            check = writer_id + "\"job\": \"Writer\"," in crew or writer_id + "\"job\": \"Story\"," in crew or writer_id + "\"job\": \"Author\"," in crew or writer_id + "\"job\": \"Screenplay\"," in crew or writer_id + "\"job\": \"Screenstory\"," in crew
            if check:
                for row3 in Normalize.iterrows():
                    if movie_id == row3[1][0]:
                        if grade < row3[1][2]:
                            grade =  row3[1][2]
                        break
        new_data = [str(row1[1][2]), writer_name, grade]
        out.writerow(new_data)
        counter += 1
        print(counter)
        if counter == 3:
            break
         

    # calculate the Producer value
    out = csv.writer(open('ProducersGrades.csv', "w", newline=''), delimiter=',', quoting=csv.QUOTE_ALL)
    data = ['ID', 'Name', 'Grade']
    out.writerow(data)
    Producers = pd.read_csv('MergedProducersFile.csv', low_memory=False)
    Normalize = pd.read_csv('Normalize.csv',usecols=['movie_id', 'budget', 'revenue'], low_memory=False)
    Movies = pd.read_csv('NewDB.csv', low_memory=False)
    counter = 0
    for row1 in Producers.iterrows():
        grade = 0
        producer_name = row1[1][0]
        producer_id = "\"id\": " + str(row1[1][2]) + ", "
        for row2 in Movies.iterrows():
            movie_id = row2[1][2]
            crew = row2[1][4]
            check = producer_id + "\"job\": \"Producer\"," in crew
            if check:
                for row3 in Normalize.iterrows():
                    if movie_id == row3[1][0]:
                        if grade < row3[1][2]:
                            grade = row3[1][2]
                        break
        new_data = [str(row1[1][2]), producer_name, grade]
        out.writerow(new_data)
        counter += 1
        print(counter)
        if counter == 9:
            break


    # calculate the Director value
    out = csv.writer(open('DirectorsGrades.csv', "w", newline=''), delimiter=',', quoting=csv.QUOTE_ALL)
    data = ['ID', 'Name', 'Grade']
    out.writerow(data)
    Directors = pd.read_csv('MergedDirectorsFile.csv', low_memory=False)
    Normalize = pd.read_csv('Normalize.csv', usecols=['movie_id', 'budget', 'revenue'], low_memory=False)
    Movies = pd.read_csv('NewDB.csv', low_memory=False)
    counter = 0
    for row1 in Directors.iterrows():
        grade = 0
        director_name = row1[1][0]
        director_id = "\"id\": " + str(row1[1][2]) + ", "
        for row2 in Movies.iterrows():
            movie_id = row2[1][2]
            crew = row2[1][4]
            check = director_id + "\"job\": \"Director\"," in crew
            if check:
                for row3 in Normalize.iterrows():
                    if movie_id == row3[1][0]:
                        if grade < row3[1][2]:
                            grade = row3[1][2] 
                        break
        new_data = [str(row1[1][2]), director_name, grade]
        out.writerow(new_data)
        counter += 1
        print(counter)
 

    # make the DBclassification for max for all
    DB = pd.read_csv('NewDB.csv', usecols=['title', 'movie_id', 'cast', 'crew'], low_memory=False)
    Normalized = pd.read_csv('Normalize.csv', usecols=['movie_id', 'budget', 'revenue'], low_memory=False)
    inDB = csv.writer(open('DBclassified.csv', "w", newline=''), delimiter=',', quoting=csv.QUOTE_ALL)
    inDB = pd.merge(DB, Normalized, on='movie_id')
    inDB.to_csv('DBclassified.csv')
    

    ########################### calculate the actors, producers, directors and writers for each movie###################

    # calculate the actors value with 3 feature for the actors
    Actors = pd.read_csv('ActorsGrades.csv', low_memory=False)
    outDB = pd.read_csv('DBclassified.csv', low_memory=False)
    
    # Actors_id_grades = csv.writer(open('Actors_id_grades.csv', "w", newline=''), delimiter=',', quoting=csv.QUOTE_ALL)
    # data = ['movie_id', 'actor1', 'actor2', 'actor3']
    # Actors_id_grades.writerow(data)
    
    with open('Actors_id_grades.csv', 'a+', newline='') as write_obj:
        Actors_id_grades = csv.writer(write_obj)

        counter = 1
        for movie in outDB.iterrows():
            if counter < 4808:
                counter += 1
                continue

            if counter == 60 or counter == 1744 or counter == 2615 or counter == 3149 or counter == 3237 or counter == 3405:
                counter += 1
                continue
            if counter == 3484 or counter == 3690 or counter == 3787 or counter == 3916 or counter == 4011 or counter == 4028:
                counter += 1
                continue
            if counter == 4087 or counter == 4124 or counter == 4137 or counter == 4159 or counter == 4266 or counter == 4323:
                counter += 1
                continue
            if counter == 4332 or counter == 4340 or counter == 4346 or counter == 4405 or counter == 4419 or counter == 4449:
                counter += 1
                continue
            if counter == 4476 or counter == 4486 or counter == 4489 or counter == 4509 or counter == 4521 or counter == 4522:
                counter += 1
                continue
            if counter == 4526 or counter == 4535 or counter == 4544 or counter == 4558 or counter == 4568 or counter == 4571:
                counter += 1
                continue
            if counter == 4580 or counter == 4582 or counter == 4584 or counter == 4589 or counter == 4592 or counter == 4599:
                counter += 1
                continue
            if counter == 4601 or counter == 4607 or counter == 4615 or counter == 4624 or counter == 4634 or counter == 4635:
                counter += 1
                continue
            if counter == 4651 or counter == 4656 or counter == 4662 or counter == 4675 or counter == 4676 or counter == 4692:
                counter += 1
                continue
            if counter == 4697 or counter == 4703 or counter == 4707 or counter == 4716 or counter == 4728 or counter == 4730:
                counter += 1
                continue
            if counter == 4734 or counter == 4755 or counter == 4773 or counter == 4775 or counter == 4796 or counter == 4797:
                counter += 1
                continue
            if counter == 4800 or counter == 4815:
                counter += 1
                continue
            movie_id = movie[1][2]
            array = movie[1].str.split(',')
            actor_id1 = array[3][4].split(':')
            actor_id2 = array[3][11].split(':')
            actor_id3 = array[3][18].split(':')
            actor1_grade = 0
            actor2_grade = 0
            actor3_grade = 0
            counter += 1
            for row in Actors.iterrows():
                if (int)(actor_id1[1]) == (int)(row[1][0]):
                    actor1_grade = row[1][2]
                    revenue_1 = (int)(row[1][2])
                if (int)(actor_id2[1]) == (int)(row[1][0]):
                    actor2_grade = row[1][2]
                if (int)(actor_id3[1]) == (int)(row[1][0]):
                    actor3_grade = row[1][2]
            # assignment
            print(counter)
            data = [movie_id, actor1_grade, actor2_grade, actor3_grade]
            Actors_id_grades.writerow(data)

   
 
    # calculate the directors value
    Directors = pd.read_csv('DirectorsGrades.csv', low_memory=False)
    Directors_id_grades = csv.writer(open('Directors_id_grades.csv', "w", newline=''), delimiter=',', quoting=csv.QUOTE_ALL)
    data = ['movie_id', 'director']
    Directors_id_grades.writerow(data)
    outDB = pd.read_csv('DBclassified.csv', usecols=['title', 'movie_id', 'cast', 'crew', 'budget', 'revenue'], low_memory=False)
    outDB.to_csv('DBclassified.csv')
    tal = 0
    for row in outDB.iterrows():           # running over movies
        directors_grade = 0
        array = row[1].str.split(',')
        size = len(array[3])/6
        num_directors = 0
        for counter in range(int(size)):   # running over the crew
            if "\"job\": \"Director\"" == array[3][4+6*counter][1:18]:
                for director in Directors.iterrows():  # running over the directors
                    director_name = director[1][1]
                    director_id = director[1][0]
                    director_grade = director[1][2]
                    if str(director_id) == array[3][4 + 6 * counter - 1][7:]:
                        num_directors += 1
                        directors_grade += director_grade
        # assignment
        if num_directors != 0:
            directors_grade = directors_grade / num_directors
        Directors_id_grades.writerow([row[1][1], directors_grade])
        tal = tal + 1
        print (tal)



    #calculate the producers value
    Producers = pd.read_csv('ProducersGrades.csv', low_memory=False)
    Producers_id_grades = csv.writer(open('Producers_id_grades.csv', "w", newline=''), delimiter=',',quoting=csv.QUOTE_ALL)
    data = ['movie_id', 'producers']
    Producers_id_grades.writerow(data)
    outDB = pd.read_csv('DBclassified.csv', usecols=['title', 'movie_id', 'cast', 'crew', 'budget', 'revenue'],
                        low_memory=False)
    outDB.to_csv('DBclassified.csv')
    tal = 0
    for row in outDB.iterrows():  # running over movies
        producers_grade = 0
        array = row[1].str.split(',')
        size = len(array[3]) / 6
        num_producers = 0
        for counter in range(int(size)):  # running over the crew
            if "\"job\": \"Producer\"" == array[3][4 + 6 * counter][1:18]:
                for producer in Producers.iterrows():  # running over the directors
                    producer_name = producer[1][1]
                    producer_id = producer[1][0]
                    producer_grade = producer[1][2]
                    if str(producer_id) == array[3][4 + 6 * counter - 1][7:]:
                        num_producers += 1
                        producers_grade += producer_grade
        # assignment
        if num_producers != 0:
            producers_grade=producers_grade/num_producers
        Producers_id_grades.writerow([row[1][1], producers_grade])
        tal = tal + 1
        print(tal)

    # calculate the writers value
    Writers = pd.read_csv('WritersGrades.csv', low_memory=False)
    Writers_id_grades = csv.writer(open('Writers_id_grades.csv', "w", newline=''), delimiter=',', quoting=csv.QUOTE_ALL)
    data = ['movie_id', 'writers']
    Writers_id_grades.writerow(data)
    outDB = pd.read_csv('DBclassified.csv', usecols=['title', 'movie_id', 'cast', 'crew', 'budget', 'revenue'],
                        low_memory=False)
    outDB.to_csv('DBclassified.csv')
    tal = 0
    for row in outDB.iterrows():  # running over movies
        writers_grade = 0
        array = row[1].str.split(',')
        size = len(array[3]) / 6
        num_writers = 0
        for counter in range(int(size)):  # running over the crew
            if "\"job\": \"Writer\"" == array[3][4 + 6 * counter][1:17] or "\"job\": \"Story\"" == array[3][4 + 6 * counter][1:15] or "\"job\": \"Author\"" == array[3][4 + 6 * counter][1:16] or "\"job\": \"Screenplay\"" == array[3][4 + 6 * counter][1:21] or "\"job\": \"Screenstory\"" == array[3][4 + 6 * counter][1:22]:
                for writer in Writers.iterrows():  # running over the directors
                    writer_name = writer[1][1]
                    writer_id = writer[1][0]
                    writer_grade = writer[1][2]
                    if str(writer_id) == array[3][4 + 6 * counter - 1][7:]:
                        num_writers += 1
                        writers_grade += writer_grade
        # assignment
        if num_writers != 0:
            writers_grade = writers_grade/num_writers
        Writers_id_grades.writerow([row[1][1], writers_grade])
        tal += 1
        print(tal)

    # merg all the files to the big DB
    DB = pd.read_csv('DBclassified.csv', usecols=['title', 'movie_id', 'cast', 'budget', 'revenue'], low_memory=False)
    Writers_id_grades = pd.read_csv('Writers_id_grades.csv')
    Producers_id_grades = pd.read_csv('Producers_id_grades.csv')
    Directors_id_grades = pd.read_csv('Directors_id_grades.csv')
    DBClassifiedFinal = csv.writer(open('DBClassifiedFinal.csv', "w", newline=''), delimiter=',', quoting=csv.QUOTE_ALL)
    DBClassifiedFinal = pd.merge(DB, Producers_id_grades, on='movie_id')
    DBClassifiedFinal = pd.merge(DBClassifiedFinal, Writers_id_grades, on='movie_id')
    DBClassifiedFinal = pd.merge(DBClassifiedFinal, Directors_id_grades, on='movie_id')
    DBClassifiedFinal.to_csv('DBClassifiedFinal.csv')











########################################################## others ######################################################
    def findTriplets(sum):
        arr = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11,
               12,
               12, 12, 13, 13, 13, 14, 14, 14, 15, 15, 15, 16, 16, 16, 17, 17, 17, 18, 18, 18, 19, 19, 19, 20, 20, 20,
               21,
               21, 21, 22, 22, 22, 23, 23, 23, 24, 24, 24, 25, 25, 25, 26, 26, 26, 27, 27, 27, 28, 28, 28, 29, 29, 29,
               30,
               30, 30]
        n = len(arr)
        numbers = list()
        for i in range(0, n - 2):
            for j in range(i + 1, n - 1):
                for k in range(j + 1, n):
                    if arr[i] + arr[j] + arr[k] == sum:
                        triple = [arr[i], arr[j], arr[k]]
                        triple.sort()
                        numbers.append(triple)
        ans = set(tuple(i) for i in numbers)
        return ans

    ans = findTriplets(9)
    print(ans)


 # calculate the actors value 
    Actors = pd.read_csv('ActorsGrades.csv', low_memory=False)
    outDB = pd.read_csv('DBclassified.csv', low_memory=False)
    counter = 0
    for movie in outDB.iterrows():
        if counter == 60 or counter == 1744 or counter == 2615 or counter == 3149 or counter == 3237 or counter == 3405:
            counter += 1
            continue
        if counter == 3484 or counter == 3690 or counter == 3787 or counter == 3916 or counter == 4011 or counter == 4028:
            counter += 1
            continue
        if counter == 4087 or counter == 4124 or counter == 4137 or counter == 4159 or counter == 4266 or counter == 4323:
            counter += 1
            continue
        if counter == 4332 or counter == 4340 or counter == 4346 or counter == 4405 or counter == 4419 or counter == 4449:
            counter += 1
            continue
        if counter == 4476 or counter == 4486 or counter == 4489 or counter == 4509 or counter == 4521 or counter == 4522:
            counter += 1
            continue
        if counter == 4526 or counter == 4535 or counter == 4544 or counter == 4558 or counter == 4568 or counter == 4571:
            counter += 1
            continue
        if counter == 4580 or counter == 4582 or counter == 4584 or counter == 4589 or  counter == 4592 or counter == 4599:
            counter += 1
            continue
        if counter == 4601 or counter == 4607 or counter == 4615 or counter == 4624 or counter == 4634 or counter == 4635:
            counter += 1
            continue
        if counter == 4651 or counter == 4656 or counter == 4662 or counter == 4675 or counter == 4676 or counter == 4692:
            counter += 1
            continue
        if counter == 4697 or counter == 4703 or counter == 4707 or counter == 4716 or counter == 4728 or counter == 4730:
            counter += 1
            continue
        if counter == 4734 or counter == 4755 or counter == 4773 or counter == 4775 or counter == 4796 or counter == 4797:
            counter += 1
            continue
        if counter == 4800 or counter == 4815:
            counter += 1
            continue
        movie_cast_grade = 0
        array = movie[1].str.split(',')
        actor_id1 = array[3][4].split(':')
        actor_id2 = array[3][11].split(':')
        actor_id3 = array[3][18].split(':')
        counter += 1
        for row in Actors.iterrows():
            if (int)(actor_id1[1]) == (int)(row[1][0]):
                movie_cast_grade += row[1][2]
                revenue_1 = (int)(row[1][2])
            if (int)(actor_id2[1]) == (int)(row[1][0]):
                movie_cast_grade += row[1][2]
            if (int)(actor_id3[1]) == (int)(row[1][0]):
                movie_cast_grade += row[1][2]
        movie_cast_grade = movie_cast_grade/3
        # assignment
        print(counter)
        outDB.loc[outDB.movie_id == movie[1][2], 'cast'] = movie_cast_grade
        outDB.to_csv('DBclassified.csv')
        
########################################################################################################################
