
package cam24Lib;

import javax.xml.bind.annotation.XmlEnum;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for ChargeType1Code.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * <p>
 * <pre>
 * &lt;simpleType name="ChargeType1Code"&gt;
 *   &lt;restriction base="{http://www.w3.org/2001/XMLSchema}string"&gt;
 *     &lt;enumeration value="BRKF"/&gt;
 *     &lt;enumeration value="COMM"/&gt;
 *   &lt;/restriction&gt;
 * &lt;/simpleType&gt;
 * </pre>
 * 
 */
@XmlType(name = "ChargeType1Code", namespace = "urn:iso:std:iso:20022:tech:xsd:camt.054.001.02")
@XmlEnum
public enum ChargeType1Code {

    BRKF,
    COMM;

    public String value() {
        return name();
    }

    public static ChargeType1Code fromValue(String v) {
        return valueOf(v);
    }

}
