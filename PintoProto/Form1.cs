using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.Linq;
using System.Net.Mail;
using System.Text;
using System.Windows.Forms;
using Microsoft.VisualBasic;

namespace PintoProto
{
    
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            button3.Visible = false;
        }

        private void Button1_Click(object sender, EventArgs e)//blur
        {
            
            label2.Text = "";
            label1.Text = "";
            //pictureBox1.Image = null;  
            button3.Visible = false;
            OpenFileDialog open = new OpenFileDialog();
            // image filters  
            open.Filter = "Image Files(*.jpg; *.jpeg; *.bmp;*.png)|*.jpg; *.jpeg; *.bmp; *.png";
            if (open.ShowDialog() == DialogResult.OK)
            {
                // image file path  
                label1.Text = open.FileName;
                //MessageBox.Show(open.FileName,"FileName");
            }

            callScript("0");
            label1.Text = "";

            // display image in picture box  
            pictureBox1.Image = new Bitmap(@"E:\Sem7\IS\Proj\PintoPrototype\temp\out.png");
            pictureBox1.SizeMode = PictureBoxSizeMode.StretchImage;

            button3.Visible = true;
            button1.Visible = false;
            
            //********************************************************************************
        }

        public string callScript(string method) {
            //******************** Script calling*****************************************
            string fileName = @"E:\Sem7\IS\Proj\PintoPrototype\run.py";    //python script to run 
            
            string image = label1.Text;
            
            #region Execute python script
            try
            {
                Process p = new Process();
                p.StartInfo = new ProcessStartInfo(@"C:\Python37\python.exe", fileName)
                {
                    Arguments = string.Format("{0} {1} {2}", fileName, method, image),//command line arguments
                    RedirectStandardOutput = true,//passing of parameters
                    UseShellExecute = false,
                    CreateNoWindow = false,//for opening script window, set it to false

                };

                p.Start();//runs the script

                string output = p.StandardOutput.ReadToEnd();//returns output of script
                p.WaitForExit();

                return output;

            }
            catch (Exception y)
            {
                MessageBox.Show(y.Message, "Error");
                return null;
            }
            #endregion
        }

        private void Button2_Click(object sender, EventArgs e)//authenticate
        {
            button3.Visible = false;
            OpenFileDialog open = new OpenFileDialog();
            // image filters  
            open.Filter = "Image Files(*.jpg; *.jpeg; *.bmp; *.png)|*.jpg; *.jpeg; *.bmp; *.png";
            if (open.ShowDialog() == DialogResult.OK)
            {
                // image file path  
                label1.Text = open.FileName;
            }

            string outp = callScript("1");

            if (outp.Contains("Authenticated")) {
                label2.Text="Authenticated";
                //MessageBox.Show("Authenticated","Original");
            }
            else if (outp.Contains("Forgery")) {
                label2.Text = "Forged";
                //MessageBox.Show("Forgery Detected","Forged");
            }
            // display image in picture box
            pictureBox1.Image = new Bitmap(label1.Text);
            pictureBox1.SizeMode = PictureBoxSizeMode.StretchImage;
        }

        public int sendMail()
        {//sends mail
            try
            {
                string receiver=Microsoft.VisualBasic.Interaction.InputBox("Enter email id:", "Email", "manan.hameed47@gmail.com");

                string sender = configuration.user;
                string pass = configuration.pass;

                MailMessage mail = new MailMessage();
                SmtpClient SmtpServer = new SmtpClient("smtp.gmail.com");

                mail.From = new MailAddress(sender);
                mail.To.Add(receiver);
                mail.Subject = "Pinto Test";
                mail.Body = "Requested picture";
                mail.Attachments.Add(new Attachment(@"E:\Sem7\IS\Proj\PintoPrototype\temp\out.png"));
                mail.Attachments.Add(new Attachment(@"E:\Sem7\IS\Proj\PintoPrototype\temp\signature"));
                mail.Attachments.Add(new Attachment(@"E:\Sem7\IS\Proj\PintoPrototype\selfsigned.crt"));
                SmtpServer.Port = 587;
                SmtpServer.Credentials = new System.Net.NetworkCredential(sender, pass);
                SmtpServer.EnableSsl = true;
                SmtpServer.Send(mail);

                return 1;
            }
            catch (Exception) {
                label2.Text = "Couldnt't send email due to technical error";
                return 0;
            }
        }

        private void Button3_Click(object sender, EventArgs e)//send mail
        {
            
            if (sendMail() == 1) {
                label2.Text = "Email sent";
                button3.Visible = false;
            }

            return;
        }
    }
}
