// gender.cpp : ¶¨Òå¿ØÖÆÌ¨Ó¦ÓÃ³ÌÐòµÄÈë¿Úµã¡£
//

//#include "stdafx.h"
#include <stdio.h>
#include "imgpcl/auto_tchar.h"
#include <opencv2/opencv.hpp>
#include <iostream>
#include <fstream>
#include <sstream>
#include <math.h>
int g_howManyPhotoForTraining = 260;//260;
//Ã¿¸öÈËÈ¡³ö8ÕÅ×÷ÎªÑµÁ·
int g_photoNumberOfOnePerson = 279;//279;
//ORLÊý¾Ý¿âÃ¿¸öÈË10ÕÅÍ¼Ïñ
using namespace cv;
using namespace std;

static Mat norm_0_255(InputArray _src)
{
    Mat src = _src.getMat();
    // ´´½¨ºÍ·µ»ØÒ»¸ö¹éÒ»»¯ºóµÄÍ¼Ïñ¾ØÕó:
    Mat dst;
    switch (src.channels())
    {
    case1:
        cv::normalize(_src, dst, 0, 255, NORM_MINMAX, CV_8UC1);
        break;
    case3:
        cv::normalize(_src, dst, 0, 255, NORM_MINMAX, CV_8UC3);
        break;
    default:
        src.copyTo(dst);
        break;
    }
    return dst;
}
//Ê¹ÓÃCSVÎÄ¼þÈ¥¶ÁÍ¼ÏñºÍ±êÇ©£¬Ö÷ÒªÊ¹ÓÃstringstreamºÍgetline·½·¨
static void read_csv(const string& filename, vector<Mat>& images, vector<int>& labels, char separator = ';')
{
    std::ifstream file(filename.c_str(), ifstream::in);
    if (!file)
    {
        string error_message = "No valid input file was given, please check the given filename.";
        CV_Error(CV_StsBadArg, error_message);
    }
    string line, path, classlabel;
    while (getline(file, line))
    {
        stringstream liness(line);
        getline(liness, path, separator);
        getline(liness, classlabel);
        if (!path.empty() && !classlabel.empty()) 
        {
            //images.push_back(imread(path, 0));
            Mat m = imread(path, 0);
            if ( m.empty() )
            {
            cout<<"aaaaaaaaa"<<endl;
                 cerr << path << " could not be read!" << endl;
                 return;
            }
            images.push_back(m);
            labels.push_back(atoi(classlabel.c_str()));
        }
    }
}

void train_and_test_pca()
{
    string fn_csv = string("/home/isi/2017_ws/src/imgpcl/gender_indexnlabel.txt");//图片索引和标签
    //string fn_csv = string("feret.txt");
    vector<Mat> allImages, train_images, test_images;
    vector<int> allLabels, train_labels, test_labels;
    try
    {
        read_csv(fn_csv, allImages, allLabels);
    }
    catch (cv::Exception& e) 
    {
        cerr << "Error opening file " << fn_csv << ". Reason: " << e.msg << endl;
        // ÎÄ¼þÓÐÎÊÌâ£¬ÎÒÃÇÉ¶Ò²×ö²»ÁËÁË£¬ÍË³öÁË
        exit(1);
    }
    if (allImages.size() <= 1) 
    {
        string error_message = "This demo needs at least 2 images to work. Please add more images to your data set!";
        CV_Error(CV_StsError, error_message);
    }

    for (int i = 0; i<allImages.size(); i++)
        equalizeHist(allImages[i], allImages[i]);
    //cout<<"AAAAAAAAAAAAAAAAAAAAAa"<<endl;
    int photoNumber = allImages.size();
    for (int i = 0; i<photoNumber; i++)
    {
        if ((i%g_photoNumberOfOnePerson)<g_howManyPhotoForTraining)
        {
            train_images.push_back(allImages[i]);
            train_labels.push_back(allLabels[i]);
        }
        else
        {
            test_images.push_back(allImages[i]);
            test_labels.push_back(allLabels[i]);
        }
    }
    //cout<<"AAAAAAAAAAAAAAAAAAAAAa"<<endl;
    Ptr<FaceRecognizer> model = createEigenFaceRecognizer();//¶¨ÒåpcaÄ£ÐÍ  
    
    model->train(train_images, train_labels);//ÑµÁ·pcaÄ£ÐÍ£¬ÕâÀïµÄmodel°üº¬ÁËËùÓÐÌØÕ÷ÖµºÍÌØÕ÷ÏòÁ¿£¬Ã»ÓÐËðÊ§  

    model->save("/home/isi/2017_ws/src/imgpcl/eigenfacepca.yml");//±£´æÑµÁ·½á¹û£¬¹©¼ì²âÊ±Ê¹ÓÃ 

    int iCorrectPrediction = 0;
    int predictedLabel;
    int testPhotoNumber = test_images.size();

    for (int i = 0; i<testPhotoNumber; i++)
    {
        predictedLabel = model->predict(test_images[i]);
        if (predictedLabel == test_labels[i])
        iCorrectPrediction++;
    }
    string result_message = format("Test Number = %d / Actual Number = %d.", testPhotoNumber, iCorrectPrediction);
    cout << result_message << endl;
    cout << "accuracy = " << float(iCorrectPrediction) / testPhotoNumber << endl;
    //cout << model->predict(imread("521.png", 0));
}
/*void test_pca()
{
    Ptr<FaceRecognizer> model = createEigenFaceRecognizer();
    model->load("eigenfacepca.yml");
    cout << model->predict(imread("/home/kris/catkin_ws/src/imgpcl/src/521.png", 0));
}
*/
int main() 
{
    cout << "pca = " << endl;
    train_and_test_pca();
    cout<<endl;
 //   test_pca();
    cin.get();
    return 0;
}
